import asyncio
import unittest
from typing import Any

from tests import _path  # noqa: F401
from bot import forms
from bot.commands import parse
from bot.relay import Relay, Routing, Who

ALICE = Who("111", "stream-a", "msg-1")
BOB = Who("222", "stream-a", "msg-2")


class FakeHangar:
    def __init__(self, turns: list[dict] | None = None) -> None:
        self.calls: list[tuple[str, dict, dict]] = []
        self.turns = turns or []
        self.elicit_with: Any = None

    async def call(self, tool: str, args: dict, who: Who, elicit: Any = None) -> dict:
        self.calls.append((tool, args, who.on_behalf_of()))
        if tool == "submit_job":
            return {"id": "job-9", "state": "queued", "url": "https://hangar.example.com/jobs/job-9"}
        if tool == "wait_for_turn":
            if self.elicit_with is not None and elicit is not None:
                self.elicited = await elicit(*self.elicit_with)
            return self.turns.pop(0) if self.turns else {"done": True}
        return {"id": args.get("job"), "state": "running"}


class FakeRoom:
    def __init__(self) -> None:
        self.posts: list[tuple[str, str]] = []

    async def post(self, stream_id: str, ml: str) -> None:
        self.posts.append((stream_id, ml))


class RelayTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.hangar, self.room = FakeHangar(), FakeRoom()
        self.relay = Relay(self.hangar, self.room, Routing(projects={"SVC": {"changeset": "example-service"}},
                                                           default={"repo": "example-org/example-service-app"}))

    async def test_ask_submits_as_the_person_with_ticket_and_change_set(self) -> None:
        await self.relay.on_message(ALICE, "@hangar do SVC-412 add the retry queue")
        tool, args, obo = self.hangar.calls[0]
        self.assertEqual(tool, "submit_job")
        self.assertEqual(args, {"instructions": "SVC-412 add the retry queue", "changeset": "example-service",
                                "ticket": "jira:SVC-412"})
        self.assertEqual(obo, {"source": "symphony", "id": "111", "reply_to": "symphony:stream-a:msg-1"})
        self.assertIn("job-9", self.room.posts[0][1])

    async def test_ask_without_a_known_project_uses_the_default_repo(self) -> None:
        await self.relay.ask(ALICE, parse("hangar fix the flaky export test"))
        self.assertEqual(self.hangar.calls[0][1], {"instructions": "fix the flaky export test",
                                                   "repo": "example-org/example-service-app"})

    async def test_events_post_to_the_asking_stream(self) -> None:
        await self.relay.on_event({"id": "e1", "type": "pr.opened", "job": "job-9", "reply_to": "symphony:stream-a:m",
                                   "links": {"pr": "https://github.com/example-org/x/pull/3"}, "summary": "SVC-412"})
        await self.relay.on_event({"id": "e2", "type": "pr.opened", "job": "job-9", "reply_to": "slack:C1:1"})
        self.assertEqual(len(self.room.posts), 1)
        self.assertIn('href="https://github.com/example-org/x/pull/3"', self.room.posts[0][1])

    async def test_approval_event_becomes_a_form_once_and_its_submit_answers_for_the_submitter(self) -> None:
        ev = {"id": "e3", "type": "turn.tool_approval", "job": "job-9", "reply_to": "symphony:stream-a:m",
              "summary": "terraform validate", "actions": [{"tool": "answer_approval",
                                                           "args": {"ref": "job-9", "approval": "ap-1"}}]}
        await self.relay.on_event(ev)
        await self.relay.on_event({**ev, "id": "e4"})
        self.assertEqual(len(self.room.posts), 1)
        self.assertIn('id="hangar:approval:job-9:ap-1"', self.room.posts[0][1])
        await self.relay.on_form(BOB, "hangar:approval:job-9:ap-1", {"action": "deny", "message": "use plan"})
        self.assertEqual(self.hangar.calls[-1], ("answer_approval",
                                                 {"ref": "job-9", "approval": "ap-1", "decision": "deny",
                                                  "message": "use plan"}, BOB.on_behalf_of()))

    async def test_needs_input_event_becomes_a_question_form(self) -> None:
        await self.relay.on_event({"id": "e5", "type": "job.needs_input", "job": "job-9",
                                   "reply_to": "symphony:stream-a:m", "summary": "Which region?"})
        self.assertIn('id="hangar:question:job-9:"', self.room.posts[0][1])
        await self.relay.on_form(ALICE, "hangar:question:job-9:", {"action": "submit", "answer": "us-central1"})
        self.assertEqual(self.hangar.calls[-1][:2], ("follow_up_job", {"job": "job-9", "message": "us-central1"}))

    async def test_live_elicitation_waits_for_the_asker_only(self) -> None:
        self.hangar.elicit_with = ("Job job-9 asks: Which region?", forms.QUESTION_SCHEMA)
        follow = asyncio.create_task(self.relay.follow(ALICE, "job-9"))
        for _ in range(50):
            await asyncio.sleep(0)
            if self.room.posts:
                break
        form_id = self.room.posts[0][1].split('form id="')[1].split('"')[0]
        self.assertTrue(form_id.startswith("hangar:elicit:job-9:"))
        await self.relay.on_form(BOB, form_id, {"action": "submit", "answer": "eu-west1"})
        self.assertIn("Only the person who asked", self.room.posts[-1][1])
        await self.relay.on_form(ALICE, form_id, {"action": "submit", "answer": "us-central1"})
        await follow
        self.assertEqual((self.hangar.elicited.action, self.hangar.elicited.content),
                         ("accept", {"answer": "us-central1"}))
        self.assertEqual(self.hangar.calls[-1][0], "wait_for_turn")  # answered inside the call, no follow_up_job

    async def test_live_elicitation_times_out_as_decline(self) -> None:
        self.relay.elicit_timeout = 0.01
        ans = await self.relay.elicit(ALICE, "job-9", "?", forms.QUESTION_SCHEMA)
        self.assertEqual(ans.action, "decline")

    async def test_invalid_submission_changes_nothing(self) -> None:
        await self.relay.on_form(ALICE, "hangar:approval:job-9:ap-2", {"action": "drop_tables"})
        self.assertEqual(self.hangar.calls, [])
        self.assertIn("Not sent", self.room.posts[-1][1])


if __name__ == "__main__":
    unittest.main()
