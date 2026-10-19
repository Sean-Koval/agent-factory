"""Symphony side: the BDK datafeed (messages and Elements form submits) and posting to streams.

Uses symphony-bdk-python as a dependency (don't fork it). Everything it receives goes straight to bot.relay.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from bot import commands
from bot.relay import Relay, Who

log = logging.getLogger("symphony-bot.listener")


class SymphonyRoom:
    def __init__(self, bdk: Any) -> None:
        self.bdk = bdk

    async def post(self, stream_id: str, message_ml: str) -> None:
        await self.bdk.messages().send_message(stream_id, message_ml)


def listener(relay: Relay, bot_user_id: int, follow: bool = True) -> Any:
    from symphony.bdk.core.service.datafeed.real_time_event_listener import RealTimeEventListener
    from symphony.bdk.core.service.message.message_parser import get_text_content_from_message

    tasks: set[asyncio.Task[Any]] = set()

    class Listener(RealTimeEventListener):
        async def on_message_sent(self, initiator: Any, event: Any) -> None:
            if initiator.user.user_id == bot_user_id:
                return
            text = get_text_content_from_message(event.message)
            if "hangar" not in text.lower():
                return
            who = Who(str(initiator.user.user_id), event.message.stream.stream_id, event.message.message_id)
            try:
                cmd = commands.parse(text)
                if cmd.verb == "ask":
                    job = await relay.ask(who, cmd)
                    if follow:  # hold wait_for_turn in the background: questions and approvals reach the room
                        task = asyncio.ensure_future(relay.follow(who, str(job["id"])))
                        tasks.add(task)
                        task.add_done_callback(tasks.discard)
                else:
                    await relay.on_message(who, text)
            except Exception as e:  # noqa: BLE001 - tell the room, keep the datafeed alive
                log.exception("ask failed")
                await relay.room.post(who.stream_id, f"<messageML>hangar refused: {type(e).__name__}</messageML>")

        async def on_symphony_elements_action(self, initiator: Any, event: Any) -> None:
            who = Who(str(initiator.user.user_id), event.stream.stream_id)
            await relay.on_form(who, event.form_id, dict(event.form_values or {}))

    return Listener()
