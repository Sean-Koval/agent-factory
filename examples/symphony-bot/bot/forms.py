"""hangar's questions and approvals as Symphony Elements forms, and their submissions back as answers.

hangar asks in two shapes, both flat JSON Schemas: an MCP elicitation while the bot holds `wait_for_turn` (the
agent's question: `{answer: string}`; a tool approval: `{decision: allow|deny|allow_always, message?}`), and the same
two as `hangar.event/v1` events (`job.needs_input`, `turn.tool_approval`) when nobody is waiting. Either way the
room gets one form; a person's submit becomes the elicitation's result, or a tool call (`answer_approval`,
`follow_up_job`) made on their behalf.

Form ids carry what the answer is for: `hangar:<kind>:<ref>:<id>`, kind `elicit`, `approval` or `question`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from typing import Any

APPROVAL_LABELS = {"allow": "Allow", "deny": "Deny", "allow_always": "Allow for this turn"}
MAX_TEXT = 4000


class InvalidSubmission(ValueError):
    """The submitted values don't satisfy the form's schema; tell the person, change nothing."""


@dataclass(frozen=True)
class FormId:
    kind: str
    ref: str
    id: str = ""

    def __str__(self) -> str:
        return f"hangar:{self.kind}:{self.ref}:{self.id}"

    @classmethod
    def parse(cls, text: str) -> FormId:
        parts = text.split(":", 3)
        if len(parts) != 4 or parts[0] != "hangar" or parts[1] not in ("elicit", "approval", "question"):
            raise InvalidSubmission(f"not a hangar form: {text[:80]}")
        return cls(parts[1], parts[2], parts[3])


@dataclass
class Answer:
    """What a submission means: an elicitation result, or a hangar tool to call for the person."""

    action: str                                    # accept | decline (elicitation), or call
    content: dict[str, Any] = field(default_factory=dict)
    tool: str | None = None
    args: dict[str, Any] = field(default_factory=dict)


def _field(name: str, prop: dict[str, Any], required: bool) -> str:
    label = escape(str(prop.get("title") or name))
    req = ' required="true"' if required else ""
    help_ = f'<p><i>{escape(str(prop["description"]))}</i></p>' if prop.get("description") else ""
    kind = prop.get("type")
    if prop.get("enum"):
        opts = "".join(f'<option value="{escape(str(v))}">{escape(str(v))}</option>' for v in prop["enum"])
        return f'{help_}<select name="{escape(name)}" label="{label}"{req}>{opts}</select>'
    if kind == "boolean":
        return f'{help_}<checkbox name="{escape(name)}" value="true">{label}</checkbox>'
    if kind == "string" and name in ("answer", "message"):
        return f'{help_}<textarea name="{escape(name)}" label="{label}"{req}></textarea>'
    return f'{help_}<text-field name="{escape(name)}" label="{label}"{req}></text-field>'


def _wrap(form_id: FormId, heading: str, body: str, fields: str, buttons: str) -> str:
    return (f'<messageML><form id="{escape(str(form_id))}"><h3>{escape(heading)}</h3><p>{escape(body)}</p>'
            f"{fields}{buttons}</form></messageML>")


def elicitation_form(form_id: FormId, message: str, schema: dict[str, Any]) -> str:
    """Any flat elicitation schema; hangar's approval schema gets one button per decision instead of a select."""
    props: dict[str, Any] = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    decision = props.get("decision") or {}
    if decision.get("enum"):
        fields = "".join(_field(n, p, n in required) for n, p in props.items() if n != "decision")
        secondary = ' class="secondary"'
        buttons = "".join(f'<button name="{escape(v)}" type="action"{secondary if i else ""}>'
                          f"{escape(APPROVAL_LABELS.get(v, v))}</button>" for i, v in enumerate(decision["enum"]))
    else:
        fields = "".join(_field(n, p, n in required) for n, p in props.items())
        buttons = ('<button name="submit" type="action">Send</button>'
                   '<button name="decline" type="action" class="secondary">Decline</button>')
    return _wrap(form_id, "hangar asks", message, fields, buttons)


APPROVAL_SCHEMA = {"type": "object", "required": ["decision"], "properties": {
    "decision": {"type": "string", "enum": ["allow", "deny", "allow_always"]},
    "message": {"type": "string", "title": "Note to the agent", "description": "Optional; sent with a denial."}}}
QUESTION_SCHEMA = {"type": "object", "required": ["answer"], "properties": {
    "answer": {"type": "string", "title": "Your answer"}}}


def approval_form(ref: str, approval: dict[str, Any], label: str) -> str:
    """A pending tool approval (`pending_approvals[]` or a `turn.tool_approval` event)."""
    tool = approval.get("tool") or "a tool"
    text = f"{label}: the agent asks to use {tool}: {approval.get('detail') or ''}".strip()
    return elicitation_form(FormId("approval", ref, str(approval["id"])), text, APPROVAL_SCHEMA)


def question_form(ref: str, question: str, label: str) -> str:
    return elicitation_form(FormId("question", ref), f"{label} asks: {question}", QUESTION_SCHEMA)


def content(schema: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """The submitted values as the elicitation's `content`: only the schema's keys, typed, required ones present."""
    props: dict[str, Any] = schema.get("properties") or {}
    out: dict[str, Any] = {}
    for name, prop in props.items():
        v = values.get(name)
        if name == "decision" and prop.get("enum") and values.get("action") in prop["enum"]:
            v = values["action"]  # the button pressed is the decision
        if isinstance(v, list):  # Elements returns a checkbox's checked values as a list
            v = v[0] if v else None
        if v in (None, ""):
            continue
        kind = prop.get("type")
        try:
            if kind == "boolean":
                v = str(v).lower() in ("true", "1", "yes", "on")
            elif kind == "integer":
                v = int(v)
            elif kind == "number":
                v = float(v)
            else:
                v = str(v)[:MAX_TEXT]
        except ValueError:
            raise InvalidSubmission(f"{prop.get('title') or name} must be a {kind}") from None
        if prop.get("enum") and v not in prop["enum"]:
            raise InvalidSubmission(f"{prop.get('title') or name} must be one of {', '.join(map(str, prop['enum']))}")
        out[name] = v
    if missing := [n for n in schema.get("required") or [] if n not in out]:
        raise InvalidSubmission(f"missing: {', '.join(missing)}")
    return out


def answer(form_id: str, values: dict[str, Any], schema: dict[str, Any] | None = None) -> Answer:
    """A submission of a form this module rendered. `schema` is the live elicitation's, for kind `elicit`."""
    fid = FormId.parse(form_id)
    if fid.kind == "elicit":
        if values.get("action") == "decline":
            return Answer("decline")
        return Answer("accept", content(schema or {}, values))
    if fid.kind == "approval":
        c = content(APPROVAL_SCHEMA, values)
        args = {"ref": fid.ref, "approval": fid.id, "decision": c["decision"]}
        if c.get("message"):
            args["message"] = c["message"]
        return Answer("call", tool="answer_approval", args=args)
    c = content(QUESTION_SCHEMA, values)
    return Answer("call", tool="follow_up_job", args={"job": fid.ref, "message": c["answer"]})
