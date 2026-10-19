"""Verify hangar.event/v1 webhooks from hangar's webhook notifier.

hangar signs the raw body with HMAC-SHA256 under the credential the notifier names (`secret_credential`) and sends
`X-Hangar-Signature: sha256=<hex>`, as its job callbacks do. When it also sends `X-Hangar-Timestamp` (Unix seconds),
the signed bytes are `<timestamp>.<body>` and an old timestamp is refused, so a captured request can't be replayed
later; the event id is remembered for the window, so it can't be replayed inside it either.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from collections import OrderedDict

WINDOW_SECONDS = 300


class Rejected(Exception):
    """The request is not a fresh, authentic hangar event; answer 401 and drop it."""


def sign(key: bytes, body: bytes, timestamp: str | None = None) -> str:
    material = f"{timestamp}.".encode() + body if timestamp is not None else body
    return "sha256=" + hmac.new(key, material, hashlib.sha256).hexdigest()


def verify(key: bytes, body: bytes, signature: str | None, timestamp: str | None = None, *,
           now: float | None = None, window: int = WINDOW_SECONDS) -> None:
    if not key:
        raise Rejected("no webhook key configured")
    if not signature or not signature.startswith("sha256="):
        raise Rejected("missing or malformed X-Hangar-Signature")
    if timestamp is not None:
        try:
            age = (time.time() if now is None else now) - int(timestamp)
        except ValueError:
            raise Rejected("malformed X-Hangar-Timestamp") from None
        if abs(age) > window:
            raise Rejected("stale X-Hangar-Timestamp")
    if not hmac.compare_digest(sign(key, body, timestamp), signature):
        raise Rejected("signature does not match")


class Seen:
    """Event ids already handled, for `window` seconds (bounded, oldest dropped first)."""

    def __init__(self, window: int = WINDOW_SECONDS, limit: int = 10_000) -> None:
        self.window, self.limit = window, limit
        self._ids: OrderedDict[str, float] = OrderedDict()

    def first_time(self, event_id: str, now: float | None = None) -> bool:
        t = time.time() if now is None else now
        while self._ids and (len(self._ids) >= self.limit or next(iter(self._ids.values())) < t - self.window):
            self._ids.popitem(last=False)
        if event_id in self._ids:
            return False
        self._ids[event_id] = t
        return True
