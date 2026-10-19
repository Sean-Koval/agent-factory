"""What a person can say to the bot, parsed from a Symphony message's text."""

from __future__ import annotations

import re
from dataclasses import dataclass

TICKET = re.compile(r"\b([A-Z][A-Z0-9_]{0,49}-[1-9][0-9]{0,9})\b")
_DO = re.compile(r"^\s*@?hangar\s+(?:do\s+)?(?P<ask>.+)$", re.I | re.S)
_SLASH = re.compile(r"^\s*/hangar\s+(?P<verb>status|cancel|approve|link)\b\s*(?P<arg>\S*)", re.I)


@dataclass(frozen=True)
class Command:
    verb: str                  # ask | status | cancel | approve | link | help
    text: str = ""             # the ask, for `ask`
    ticket: str | None = None  # a Jira key found in the ask: becomes ticket="jira:<KEY>"
    target: str = ""           # a job id, for status | cancel | approve


def parse(text: str) -> Command:
    text = text.strip()
    if m := _SLASH.match(text):
        return Command(m["verb"].lower(), target=m["arg"])
    if m := _DO.match(text):
        ask = m["ask"].strip()
        t = TICKET.search(ask)
        return Command("ask", text=ask, ticket=t[1] if t else None)
    return Command("help")


HELP = ("Ask me for work: <b>@hangar do SVC-412</b> or <b>@hangar fix the flaky export test in example-service</b>. "
        "Then <b>/hangar status JOB</b>, <b>/hangar cancel JOB</b>, <b>/hangar approve JOB</b> (if you may), "
        "<b>/hangar link</b> to connect your account.")
