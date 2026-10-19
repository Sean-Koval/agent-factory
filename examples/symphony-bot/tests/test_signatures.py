import json
import unittest

from tests import _path  # noqa: F401
from bot import signatures
from bot.webhook import Webhook

KEY = b"test-key-not-a-secret"


class SignatureTest(unittest.TestCase):
    def test_hangar_callback_format_verifies(self) -> None:
        body = b'{"id": "ev-1"}'
        signatures.verify(KEY, body, signatures.sign(KEY, body))

    def test_rejects_wrong_key_tampered_body_and_missing_header(self) -> None:
        body = b'{"id": "ev-1"}'
        sig = signatures.sign(KEY, body)
        for key, b, s in ((b"other", body, sig), (KEY, body + b" ", sig), (KEY, body, None), (KEY, body, "md5=x"),
                          (b"", body, sig)):
            with self.assertRaises(signatures.Rejected):
                signatures.verify(key, b, s)

    def test_timestamp_is_signed_and_bounded(self) -> None:
        body = b'{"id": "ev-2"}'
        sig = signatures.sign(KEY, body, "1000")
        signatures.verify(KEY, body, sig, "1000", now=1100)
        with self.assertRaises(signatures.Rejected):  # too old: a replay
            signatures.verify(KEY, body, sig, "1000", now=1000 + signatures.WINDOW_SECONDS + 1)
        with self.assertRaises(signatures.Rejected):  # a fresh timestamp on an old signature
            signatures.verify(KEY, body, sig, "1100", now=1100)
        with self.assertRaises(signatures.Rejected):
            signatures.verify(KEY, body, sig, "soon", now=1100)

    def test_seen_ids_expire(self) -> None:
        seen = signatures.Seen(window=10)
        self.assertTrue(seen.first_time("a", now=0))
        self.assertFalse(seen.first_time("a", now=5))
        self.assertTrue(seen.first_time("a", now=20))


class WebhookTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.got: list[dict] = []

        async def on_event(e: dict) -> None:
            self.got.append(e)

        self.hook = Webhook(KEY, on_event)

    def signed(self, event: dict, ts: str = "1000") -> tuple[dict[str, str], bytes]:
        body = json.dumps(event).encode()
        return {"x-hangar-signature": signatures.sign(KEY, body, ts), "x-hangar-timestamp": ts}, body

    async def test_signed_event_is_handled_once(self) -> None:
        h, b = self.signed({"id": "ev-1", "type": "pr.opened"})
        self.assertEqual(await self.hook.handle(h, b, now=1000), 202)
        self.assertEqual(await self.hook.handle(h, b, now=1001), 200)  # the retry: acknowledged, not re-posted
        for t in list(self.hook.tasks):
            await t
        self.assertEqual([e["id"] for e in self.got], ["ev-1"])

    async def test_unsigned_or_forged_runs_nothing(self) -> None:
        h, b = self.signed({"id": "ev-2"})
        self.assertEqual(await self.hook.handle({}, b, now=1000), 401)
        self.assertEqual(await self.hook.handle(h, b.replace(b"ev-2", b"ev-3"), now=1000), 401)
        self.assertEqual(await self.hook.handle(h, b, now=5000), 401)
        self.assertEqual(self.got, [])

    async def test_asgi_round_trip(self) -> None:
        h, b = self.signed({"id": "ev-4"})
        sent: list[dict] = []
        msgs = [{"type": "http.request", "body": b, "more_body": False}]

        async def receive() -> dict:
            return msgs.pop(0)

        async def send(m: dict) -> None:
            sent.append(m)

        scope = {"type": "http", "method": "POST", "path": "/hangar/events",
                 "headers": [(k.encode(), v.encode()) for k, v in {**h, "x-hangar-timestamp": "1000"}.items()]}
        import bot.signatures as s
        real = s.time.time
        s.time.time = lambda: 1000.0
        try:
            await self.hook(scope, receive, send)
        finally:
            s.time.time = real
        self.assertEqual(sent[0]["status"], 202)


if __name__ == "__main__":
    unittest.main()
