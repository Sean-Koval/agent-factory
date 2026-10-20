"""hangar's MCP over streamable HTTP (the `mcp` SDK), one short session per call, as the person it is for.

The bot's hangar token has the `relay` scope; each session carries `X-Hangar-On-Behalf-Of` (the Symphony user and
where to reply), so hangar resolves the person through their `symphony:` link and audits both identities. A
session holding `wait_for_turn` answers hangar's elicitations with the room's form (bot.relay).
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from bot import forms
from bot.relay import Who


class HangarRefused(RuntimeError):
    """hangar answered with an error (a refused relay, an unknown job, a scope it won't grant)."""


def _leaf(e: BaseException) -> BaseException:
    while isinstance(e, BaseExceptionGroup) and e.exceptions:  # the SDK's task group wraps transport errors
        e = e.exceptions[0]
    return e


class HangarClient:
    def __init__(self, url: str, token: str, timeout_seconds: float = 180.0) -> None:
        self.url = url.rstrip("/") + "/mcp"
        self.token, self.timeout = token, timeout_seconds
        self.server_version: str | None = None  # hangar's serverInfo.version: the MCP surface this bot was tested on

    def headers(self, who: Who) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "X-Hangar-On-Behalf-Of": json.dumps(who.on_behalf_of())}

    async def call(self, tool: str, args: dict[str, Any], who: Who, elicit: Any = None) -> dict[str, Any]:
        from mcp import ClientSession, types  # mcp 1.x (pyproject), imported here: the core runs without it
        from mcp.client.streamable_http import streamablehttp_client

        async def on_elicit(_ctx: Any, params: types.ElicitRequestParams) -> types.ElicitResult:
            if elicit is None:
                return types.ElicitResult(action="decline")
            ans: forms.Answer = await elicit(params.message, dict(getattr(params, "requestedSchema", None) or {}))
            if ans.action == "accept":
                return types.ElicitResult(action="accept", content=ans.content)
            return types.ElicitResult(action=ans.action if ans.action in ("decline", "cancel") else "decline")

        try:
            async with streamablehttp_client(self.url, headers=self.headers(who), timeout=self.timeout) as (r, w, _):
                async with ClientSession(r, w, elicitation_callback=on_elicit) as session:
                    init = await session.initialize()
                    self.server_version = init.serverInfo.version
                    res = await session.call_tool(tool, args)
        except BaseException as e:  # noqa: BLE001 - an HTTP refusal arrives as an ExceptionGroup
            leaf = _leaf(e)
            if isinstance(leaf, (KeyboardInterrupt, SystemExit, asyncio.CancelledError)):
                raise
            status = getattr(getattr(leaf, "response", None), "status_code", None)  # a streamed body isn't read
            raise HangarRefused(f"hangar {tool}: " + (f"HTTP {status}" if status else f"{type(leaf).__name__}: {leaf}")
                                ) from leaf
        if res.isError:
            text = " ".join(getattr(c, "text", "") for c in res.content)
            raise HangarRefused(f"hangar {tool}: {text.strip() or 'error'}")
        if res.structuredContent is not None:
            return dict(res.structuredContent)
        text = "".join(getattr(c, "text", "") for c in res.content)
        return json.loads(text) if text.strip().startswith("{") else {"text": text}
