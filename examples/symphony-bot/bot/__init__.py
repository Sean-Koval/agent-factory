"""A Symphony bot that puts hangar's MCP front door in a room (agent-factory examples/symphony-bot).

The core modules (commands, forms, signatures, relay, webhook) use the standard library only and hold every
decision; `listener` (Symphony BDK) and `hangar_client` (the `mcp` SDK) are thin adapters around them.
"""
