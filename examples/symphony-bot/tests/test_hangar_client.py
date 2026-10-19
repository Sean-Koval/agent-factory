"""HangarClient against a real streamable-HTTP MCP server built with the same SDK (skipped without `mcp`).

The server stands in for hangar's /mcp: it records the headers each session carries, answers submit_job, asks an
elicitation from wait_for_turn, and refuses a bad token with 403 as hangar's auth middleware does.
"""

import asyncio
import json
import socket
import threading
import time
import unittest

from tests import _path  # noqa: F401

try:
    from importlib.metadata import version

    if int(version("mcp").split(".")[0]) >= 2:
        raise ImportError(f"mcp {version('mcp')}: the bot pins mcp<2")
    import uvicorn
    from mcp.server.fastmcp import Context, FastMCP
    from pydantic import BaseModel
except Exception as e:  # noqa: BLE001 - not installed, or not the pinned major
    raise unittest.SkipTest(f"needs the bot's dependencies (pip install -e .): {e}") from None

from bot import forms  # noqa: E402
from bot.hangar_client import HangarClient, HangarRefused  # noqa: E402
from bot.relay import Who  # noqa: E402

SEEN: list[dict] = []


class Answer(BaseModel):
    answer: str


def server() -> FastMCP:
    mcp = FastMCP("hangar-standin")

    @mcp.tool()
    async def submit_job(instructions: str, ctx: Context, changeset: str | None = None,
                         ticket: str | None = None, repo: str | None = None) -> dict:
        h = ctx.request_context.request.headers
        SEEN.append({"obo": json.loads(h["x-hangar-on-behalf-of"]), "auth": h["authorization"]})
        return {"id": "job-1", "state": "queued", "changeset": changeset, "ticket": ticket}

    @mcp.tool()
    async def wait_for_turn(ref: str, ctx: Context) -> dict:
        res = await ctx.elicit(f"Job {ref} asks: which region?", schema=Answer)
        return {"done": True, "elicitation": res.action, "answer": res.data.answer if res.action == "accept" else None}

    return mcp


def refuse_bad_tokens(app):
    async def wrapped(scope, receive, send):
        if scope["type"] == "http" and dict(scope["headers"]).get(b"authorization") != b"Bearer hgr_good":
            await send({"type": "http.response.start", "status": 403,
                        "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": b"relay token required"})
            return
        await app(scope, receive, send)
    return wrapped


class HangarClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            cls.port = s.getsockname()[1]
        cfg = uvicorn.Config(refuse_bad_tokens(server().streamable_http_app()), host="127.0.0.1", port=cls.port,
                             log_level="warning", lifespan="on")
        cls.srv = uvicorn.Server(cfg)
        cls.thread = threading.Thread(target=cls.srv.run, daemon=True)
        cls.thread.start()
        for _ in range(100):
            if cls.srv.started:
                break
            time.sleep(0.05)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.srv.should_exit = True
        cls.thread.join(5)

    def client(self, token: str = "hgr_good") -> HangarClient:
        return HangarClient(f"http://127.0.0.1:{self.port}", token, timeout_seconds=10)

    def test_submit_carries_the_relay_token_and_on_behalf_of(self) -> None:
        who = Who("111", "stream-a", "msg-1")
        job = asyncio.run(self.client().call("submit_job", {"instructions": "x", "changeset": "example-service",
                                                            "ticket": "jira:SVC-1"}, who))
        self.assertEqual((job["id"], job["changeset"], job["ticket"]), ("job-1", "example-service", "jira:SVC-1"))
        self.assertEqual(SEEN[-1], {"auth": "Bearer hgr_good", "obo": who.on_behalf_of()})

    def test_elicitation_is_answered_by_the_room(self) -> None:
        asked = []

        async def elicit(message: str, schema: dict) -> forms.Answer:
            asked.append((message, schema))
            return forms.answer("hangar:elicit:job-1:k", {"action": "submit", "answer": "us-central1"}, schema)

        turn = asyncio.run(self.client().call("wait_for_turn", {"ref": "job-1"}, Who("111", "s"), elicit=elicit))
        self.assertEqual((turn["elicitation"], turn["answer"]), ("accept", "us-central1"))
        self.assertIn("answer", asked[0][1]["properties"])

    def test_no_elicitor_declines(self) -> None:
        turn = asyncio.run(self.client().call("wait_for_turn", {"ref": "job-1"}, Who("111", "s")))
        self.assertEqual(turn["elicitation"], "decline")

    def test_a_refusal_is_one_readable_error(self) -> None:
        with self.assertRaisesRegex(HangarRefused, "HTTP 403"):
            asyncio.run(self.client("hgr_bad").call("submit_job", {"instructions": "x"}, Who("111", "s")))


if __name__ == "__main__":
    unittest.main()
