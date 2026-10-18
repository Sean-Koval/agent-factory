<span class="af-eyebrow">Airframe</span>

# Registry

Airframe is also a [shadcn-compatible registry](https://ui.shadcn.com/docs/registry), so one command puts its files into any project: a Python console, a Vite app, a Tailwind project or a bare folder a coding agent is working in. The items are *universal*: every file has an explicit target, and nothing needs React, Tailwind or a `components.json`. The tool repos keep using `scripts/sync-airframe.sh theme-vN`, which does the same job with a fixed destination list; the registry is for everything else.

## Install

From this site (built JSON, always the current release):

```sh
npx shadcn@latest add https://sean-koval.github.io/agent-factory/r/airframe.json
```

From the repository, pinned to a release tag (a [GitHub source registry](https://ui.shadcn.com/docs/registry/github); the CLI reads `registry.json` at the repo root):

```sh
npx shadcn@latest add Sean-Koval/agent-factory/airframe#theme-v4
npx shadcn@latest add Sean-Koval/agent-factory/skill#theme-v4
npx shadcn@latest list Sean-Koval/agent-factory
```

A `#ref` pins the item you name; the CLI does not carry it to that item's dependencies, which it reads from `main`. So `button#theme-v4` installs that tag's contract but the current `airframe` files. Pin the whole set by naming every item in one command, or install from the site, where each release's items are built together.

As a named registry, for the `shadcn` MCP server and `@airframe/<item>` addresses (needs a full `components.json`):

```json
{ "registries": { "@airframe": "https://sean-koval.github.io/agent-factory/r/{name}.json" } }
```

## Items

| Item | What it installs |
| --- | --- |
| `airframe` | The three files the tool repos vendor: tokens, `af-` classes, icon sprite, under `airframe/`. For any web UI. |
| `airframe-tailwind` | The tokens plus `airframe-tailwind.css`, a Tailwind v4 `@theme` over them: `bg-canvas`, `text-fg-muted`, `font-display`, `text-label`, `rounded-card`, and no default palette. |
| `airframe-tokens` | `airframe.tokens.json` (Night) and `airframe-day.tokens.json` (Day) in the [W3C Design Tokens format](https://www.designtokens.org/tr/drafts/format/), plus the resolved `airframe-tokens.json`. For Figma variables, Style Dictionary, Terrazzo and scripts that draw. |
| `skill` | The Airframe skill for coding agents, at `.claude/skills/airframe/` (Claude Code) and `.agents/skills/airframe/` (Codex): the rules, the classes, where each contract lives. |
| `button`, `status`, `card`, `fleet-bay` | The component's contract as `airframe/components/<Name>.md`, next to the code; each depends on `airframe`. |
| `react` | `src/components/airframe/{Button,Status,Card,Icon}.tsx`: thin wrappers that only compose `af-` classes. A prototype; the consoles are vanilla JS. |

The source is [`registry.json`](https://github.com/Sean-Koval/agent-factory/blob/main/registry.json) at the repository root; `python3 scripts/airframe.py registry DIR` inlines each item's files into `DIR/<item>.json`, which this site serves under `/r/`. `python3 scripts/airframe.py check` validates the registry with the rest of Airframe.
