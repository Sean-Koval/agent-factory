"""POST /hangar/events: hangar.event/v1 from hangar's webhook notifier, as a plain ASGI app (run it with any ASGI
server, e.g. `uvicorn bot.webhook:app` after `configure`)."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from bot import signatures

log = logging.getLogger("symphony-bot.webhook")
MAX_BODY = 1 << 20


class Webhook:
    def __init__(self, key: bytes, on_event: Any, path: str = "/hangar/events") -> None:
        self.key, self.on_event, self.path = key, on_event, path
        self.seen = signatures.Seen()
        self.tasks: set[asyncio.Task[None]] = set()

    async def handle(self, headers: dict[str, str], body: bytes, now: float | None = None) -> int:
        """The HTTP status to answer. Verifies first; never runs anything for an unsigned or replayed body."""
        try:
            signatures.verify(self.key, body, headers.get("x-hangar-signature"), headers.get("x-hangar-timestamp"),
                              now=now)
        except signatures.Rejected as e:
            log.warning("rejected a webhook: %s", e)
            return 401
        try:
            event = json.loads(body)
        except ValueError:
            return 400
        if not isinstance(event, dict) or not event.get("id"):
            return 400
        if not self.seen.first_time(str(event["id"]), now):
            return 200  # a retry of one we already have: acknowledge, do nothing
        task = asyncio.ensure_future(self.on_event(event))  # answer hangar at once; posting can be slow
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return 202

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            return
        status = 404
        if scope.get("path") == self.path and scope.get("method") == "POST":
            headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers") or []}
            body, more = b"", True
            while more and len(body) <= MAX_BODY:
                msg = await receive()
                body += msg.get("body", b"")
                more = msg.get("more_body", False)
            status = 413 if len(body) > MAX_BODY else await self.handle(headers, body)
        await send({"type": "http.response.start", "status": status, "headers": [(b"content-length", b"0")]})
        await send({"type": "http.response.body", "body": b""})
