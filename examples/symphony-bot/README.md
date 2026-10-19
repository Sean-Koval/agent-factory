# Symphony bot (template)

A copy-me starter that puts hangar's MCP front door in Symphony rooms. A person says `@hangar do SVC-412`; the bot
calls hangar's `submit_job` **on their behalf**; hangar's questions and tool approvals come back to the room as
Elements forms; pull requests opened, landed and deployed come back as messages. hangar stays the gate: the bot holds
no rules of its own, and every answer is checked by hangar against the person who gave it.

Copy this directory into your bot repo (`agent-factory-bots/symphony-bot/` in the
[company overlay](../company-overlay/)), fill in `config.yaml`, and pin the hangar MCP surface you tested against
(the `serverInfo.version` hangar reports, which `HangarClient.server_version` records). It has no hangar code
dependency and nothing company-specific; site values live only in your `config.yaml`.

```text
bot/
  commands.py       what people can say: "@hangar do <ask>", /hangar status|cancel|approve|link
  relay.py          asks to jobs, hangar's questions and approvals to forms, events to messages
  forms.py          elicitation schemas to Elements forms, submissions back to answers or hangar calls
  signatures.py     X-Hangar-Signature (HMAC-SHA256) and replay checks for hangar.event/v1 webhooks
  webhook.py        POST /hangar/events, as a plain ASGI app
  hangar_client.py  hangar's MCP over streamable HTTP (the mcp SDK), as the person a call is for
  listener.py       the Symphony BDK datafeed: messages and form submits
  config.py         config.yaml
config.example.yaml
tests/              stdlib only: python -m unittest discover -s tests -t .
```

## How it talks to hangar

| Direction | How | hangar side |
| --- | --- | --- |
| Ask | `submit_job(instructions, changeset=…, ticket="jira:SVC-412")` or `repo=…`, routed by the ticket's Jira project (`routing` in `config.yaml`) | MCP at `/mcp`; `changeset` and `ticket` are the change-set arguments |
| Who | A token with the `relay` scope, plus `X-Hangar-On-Behalf-Of: {"source": "symphony", "id": <userId>, "reply_to": "symphony:<stream>:<message>"}` on each session | hangar resolves the user through their `symphony:` person link; an unlinked user's job needs approval, or is refused, per hangar's setting |
| Questions, live | The bot holds `wait_for_turn`; hangar's elicitation becomes a form, and only the asker's submit answers it | `wait_for_turn` elicits the agent's question and tool approvals |
| Questions, later | `job.needs_input` and `turn.tool_approval` events become forms; a submit calls `follow_up_job` or `answer_approval` as the person who submitted | hangar refuses what that person may not do |
| Events | hangar's webhook notifier posts `hangar.event/v1` to `/hangar/events`, signed with the credential `bot-hook-key`; the bot posts to the event's `reply_to` stream | `HANGAR_PLUGINS.notifiers.webhook` in your deploy repo |
| Approvals | `/hangar approve JOB` calls `approve_job` as the person; hangar allows it only for relay tokens with `relay_may_approve` and never on the person's own job | hangar's approval rules |

The mapping from Symphony users to hangar people is hangar's: `hangar person link alice symphony <userId>`. `/hangar
link` tells a person what to ask their admin.

## Run it

```sh
pip install -e .                      # symphony-bdk-python, mcp, uvicorn, pyyaml: pin what you qualified
python -m bot config.yaml             # the datafeed and the webhook endpoint (port 8080) in one process
python -m unittest discover -s tests -t .
```

Give it a hangar token with the `relay` scope and the webhook key from your secret manager (both files, named in
`config.yaml`), and make `/hangar/events` reachable from hangar only. If hangar can't reach the bot, subscribe to
hangar's `hangar://events` resource instead of exposing the webhook.

## What is settled and what isn't

The form shapes follow hangar's elicitation schemas today (tool approvals: `decision` allow, deny or allow_always and
an optional `message`; questions: `answer`), and the signature is the `sha256=<hex>` HMAC hangar's job callbacks
already send. The relay scope, `X-Hangar-On-Behalf-Of`, the `symphony` link source, the event types, the
`X-Hangar-Timestamp` replay header and the `changeset` and `ticket` arguments are hangar's plugin, identity and
change-set work in progress; check them against the hangar release you pin.
