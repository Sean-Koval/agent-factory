"""The room side of hangar: asks become jobs, hangar's questions and approvals become forms, events become messages.

Every hangar call is made on behalf of the Symphony user it is for (`on_behalf_of`), so the job is that person's,
counts against their caps and shows up in their list; hangar decides what they may do (approve, answer), never the
bot. The bot holds no mapping of its own: `hangar person link <person> symphony <userId>` is the mapping.
"""

from __future__ import annotations

import asyncio
import logging
import secrets
from dataclasses import dataclass, field
from html import escape
from typing import Any, Protocol

from bot import commands, forms

log = logging.getLogger("symphony-bot.relay")


@dataclass(frozen=True)
class Who:
    """A Symphony user, and the message they spoke in (where replies go)."""

    user_id: str
    stream_id: str
    message_id: str = ""

    def on_behalf_of(self) -> dict[str, str]:
        return {"source": "symphony", "id": self.user_id,
                "reply_to": f"symphony:{self.stream_id}:{self.message_id}"}


class Hangar(Protocol):
    async def call(self, tool: str, args: dict[str, Any], who: Who, elicit: Any = None) -> dict[str, Any]: ...


class Room(Protocol):
    async def post(self, stream_id: str, message_ml: str) -> None: ...


@dataclass
class Routing:
    """Where an ask goes, from config.yaml: a Jira project key to a change-set profile or a repo."""

    projects: dict[str, dict[str, str]] = field(default_factory=dict)  # {"SVC": {"changeset": "example-service"}}
    default: dict[str, str] = field(default_factory=dict)              # {"repo": "example-org/example-service-app"}

    def target(self, cmd: commands.Command) -> dict[str, str]:
        if cmd.ticket and (hit := self.projects.get(cmd.ticket.split("-", 1)[0])):
            return dict(hit)
        return dict(self.default)


def _ml(text: str) -> str:
    return f"<messageML>{text}</messageML>"


def _link(url: str | None, label: str) -> str:
    return f'<a href="{escape(url)}">{escape(label)}</a>' if url else escape(label)


class Relay:
    def __init__(self, hangar: Hangar, room: Room, routing: Routing | None = None,
                 elicit_timeout: float = 600.0) -> None:
        self.hangar, self.room, self.routing = hangar, room, routing or Routing()
        self.elicit_timeout = elicit_timeout
        self._waiting: dict[str, tuple[Who, dict[str, Any], asyncio.Future[forms.Answer]]] = {}
        self._posted: set[str] = set()  # approval ids already in the room

    # ------------------------------------------------------------------ asks
    async def on_message(self, who: Who, text: str) -> None:
        cmd = commands.parse(text)
        if cmd.verb == "ask":
            await self.ask(who, cmd)
        elif cmd.verb in ("status", "cancel", "approve") and cmd.target:
            tool = {"status": "get_job", "cancel": "cancel_job", "approve": "approve_job"}[cmd.verb]
            job = await self.hangar.call(tool, {"job": cmd.target}, who)
            await self.room.post(who.stream_id, _ml(f"{escape(job.get('id', cmd.target))}: "
                                                    f"{escape(str(job.get('state', '')))}"))
        elif cmd.verb == "link":
            await self.room.post(who.stream_id, _ml(
                "Ask a hangar admin to run: <code>hangar person link YOUR-PERSON symphony "
                f"{escape(who.user_id)}</code>. Until then your asks need an approval."))
        else:
            await self.room.post(who.stream_id, _ml(commands.HELP))

    async def ask(self, who: Who, cmd: commands.Command) -> dict[str, Any]:
        """submit_job for the person; the job, or {} when hangar refused (the room is told why)."""
        args: dict[str, Any] = {"instructions": cmd.text, **self.routing.target(cmd)}
        if cmd.ticket:
            args["ticket"] = f"jira:{cmd.ticket}"
        try:
            job = await self.hangar.call("submit_job", args, who)
        except Exception as e:  # noqa: BLE001 - hangar refused (unlinked, no ticket, over a cap): say so in the room
            await self.room.post(who.stream_id, _ml(
                f"hangar didn't start it: {escape(str(e)[:400])}. If your account isn't linked yet, "
                "<b>/hangar link</b> says how."))
            return {}
        await self.room.post(who.stream_id, _ml(
            f"Started {_link(job.get('url'), job.get('id', 'a job'))} for you: {escape(job.get('state', 'queued'))}. "
            "I'll post its questions, approvals and PRs here."))
        return job

    async def follow(self, who: Who, job_id: str, max_turns: int = 1000) -> dict[str, Any]:
        """Hold wait_for_turn until the job's turn ends; hangar's elicitations come to `elicit` meanwhile."""
        turn: dict[str, Any] = {}
        for _ in range(max_turns):
            turn = await self.hangar.call("wait_for_turn", {"ref": job_id}, who, elicit=self.elicitor(who, job_id))
            for a in turn.get("pending_approvals") or []:
                await self.post_approval(who.stream_id, job_id, a, f"Job {job_id}")
            if turn.get("done"):
                break
        if (q := turn.get("question")) and turn.get("elicitation") != "answered":
            await self.room.post(who.stream_id, forms.question_form(job_id, str(q), f"Job {job_id}"))
        elif turn.get("summary"):
            await self.room.post(who.stream_id, _ml(f"{escape(job_id)}: {escape(str(turn['summary']))}"))
        return turn

    # ------------------------------------------------------------------ forms
    def elicitor(self, who: Who, ref: str) -> Any:
        async def elicit(message: str, schema: dict[str, Any]) -> forms.Answer:
            return await self.elicit(who, ref, message, schema)
        return elicit

    async def elicit(self, who: Who, ref: str, message: str, schema: dict[str, Any]) -> forms.Answer:
        """A live MCP elicitation: post the form, wait for the asker's submit (or decline on timeout)."""
        fid = forms.FormId("elicit", ref, secrets.token_hex(6))
        fut: asyncio.Future[forms.Answer] = asyncio.get_running_loop().create_future()
        self._waiting[str(fid)] = (who, schema, fut)
        try:
            await self.room.post(who.stream_id, forms.elicitation_form(fid, message, schema))
            return await asyncio.wait_for(fut, self.elicit_timeout)
        except TimeoutError:
            return forms.Answer("decline")
        finally:
            self._waiting.pop(str(fid), None)

    async def post_approval(self, stream_id: str, ref: str, approval: dict[str, Any], label: str) -> None:
        if (aid := str(approval.get("id"))) in self._posted:
            return
        self._posted.add(aid)
        await self.room.post(stream_id, forms.approval_form(ref, approval, label))

    async def on_form(self, who: Who, form_id: str, values: dict[str, Any]) -> None:
        """A person submitted one of our forms. Live elicitations accept only the asker (it is their session);
        any other answer is a hangar call on behalf of whoever submitted, and hangar decides if they may."""
        try:
            waiting = self._waiting.get(form_id)
            if waiting is not None:
                asker, schema, fut = waiting
                if who.user_id != asker.user_id:
                    await self.room.post(who.stream_id, _ml("Only the person who asked can answer this one."))
                    return
                if not fut.done():
                    fut.set_result(forms.answer(form_id, values, schema))
                return
            ans = forms.answer(form_id, values)
            if ans.tool is None:  # an elicitation nobody waits for any more (timed out, or the bot restarted)
                await self.room.post(who.stream_id, _ml("That question has expired; ask again with /hangar status."))
                return
            await self.hangar.call(ans.tool, ans.args, who)
            await self.room.post(who.stream_id, _ml("Sent to hangar."))
        except forms.InvalidSubmission as e:
            await self.room.post(who.stream_id, _ml(f"Not sent: {escape(str(e))}"))

    # ------------------------------------------------------------------ events (webhook or hangar://events)
    async def on_event(self, event: dict[str, Any]) -> None:
        reply_to = str(event.get("reply_to") or "")
        if not reply_to.startswith("symphony:"):
            return  # not asked from Symphony: nowhere to post
        stream_id = reply_to.split(":")[1]
        kind, job = str(event.get("type", "")), str(event.get("job") or "")
        links: dict[str, str] = event.get("links") or {}
        summary = str(event.get("summary") or "")
        if kind == "turn.tool_approval":
            for act in event.get("actions") or []:
                if act.get("tool") == "answer_approval":
                    a = act.get("args") or {}
                    await self.post_approval(stream_id, str(a.get("ref") or job),
                                             {"id": a.get("approval"), "tool": a.get("tool"), "detail": summary},
                                             f"Job {job}")
            return
        if kind == "job.needs_input":
            await self.room.post(stream_id, forms.question_form(job, summary, f"Job {job}"))
            return
        text = {
            "pr.opened": "opened a pull request", "pr.landed": "landed", "pr.closed": "closed a pull request",
            "job.failed": "failed", "job.finished": "finished", "job.queued": "is queued",
            "changeset.done": "deployed: the change set is done",
            "changeset.broken": "stopped: the change set is broken",
        }.get(kind) or (kind.replace(".", " ") if kind.startswith("changeset.") else "")
        if not text:
            return
        link = links.get("pr") or links.get("job")
        await self.room.post(stream_id, _ml(f"{_link(link, job or 'hangar')} {escape(text)}"
                                            + (f": {escape(summary)}" if summary else "")))
