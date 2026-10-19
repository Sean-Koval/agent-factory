"""python -m bot config.yaml: the datafeed and the webhook endpoint in one process."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from bot.config import load
from bot.hangar_client import HangarClient
from bot.listener import SymphonyRoom, listener
from bot.relay import Relay
from bot.webhook import Webhook


async def main(path: str) -> None:
    import uvicorn
    from symphony.bdk.core.config.loader import BdkConfigLoader
    from symphony.bdk.core.symphony_bdk import SymphonyBdk

    cfg = load(Path(path))
    async with SymphonyBdk(BdkConfigLoader.load_from_file(cfg.bdk_config)) as bdk:
        relay = Relay(HangarClient(cfg.hangar_url, cfg.secret("hangar_token")), SymphonyRoom(bdk), cfg.routing)
        me = await bdk.sessions().get_session()
        feed = bdk.datafeed()
        feed.subscribe(listener(relay, me.id))
        hook = Webhook(cfg.secret("webhook_key").encode(), relay.on_event)
        server = uvicorn.Server(uvicorn.Config(hook, host="0.0.0.0", port=cfg.webhook_port, log_level="info"))
        await asyncio.gather(feed.start(), server.serve())


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "config.yaml"))
