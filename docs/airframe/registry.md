<span class="af-eyebrow">Airframe</span>

# Registry

Airframe is also a [shadcn-compatible registry](https://ui.shadcn.com/docs/registry), so one command puts its files into any project. That can be a Python console, a Vite app, a Tailwind project or a bare folder a coding agent is working in.

The items are *universal*. Every file has an explicit target, and nothing needs React, Tailwind or a `components.json`.

## Install

There are three ways in. Pick the first unless you need a pinned tag or `@airframe/<item>` addresses.

### From this site

The built JSON is always the current release, and each release's items are built together.

```sh
npx shadcn@latest add https://sean-koval.github.io/agent-factory/r/airframe.json
```

### From the repository, pinned

This is a [GitHub source registry](https://ui.shadcn.com/docs/registry/github): the CLI reads `registry.json` at the repo root. The `#ref` pins the release.

--8<-- "airframe-install.md"

### As a named registry

For the `shadcn` MCP server and `@airframe/<item>` addresses. This one needs a full `components.json`.

```json
{ "registries": { "@airframe": "https://sean-koval.github.io/agent-factory/r/{name}.json" } }
```

!!! note "Working in a tool repo?"
    hangar, flightdeck, ai-dlc and Tower keep using `scripts/sync-airframe.sh theme-vN`, which does the same job with a fixed destination list. The registry is for everything else.

## Items

Swap `airframe` in any command above for one of these names.

### The system

| Item | What it installs |
| --- | --- |
| `airframe` | The three files the tool repos vendor, under `airframe/`: tokens, `af-` classes and the icon sprite. For any web UI. |
| `airframe-tailwind` | The tokens plus `airframe-tailwind.css`, a Tailwind v4 `@theme` over them: `bg-canvas`, `text-fg-muted`, `font-display`, `text-label`, `rounded-card`, and no default palette. |
| `airframe-tokens` | `airframe.tokens.json` (Night) and `airframe-day.tokens.json` (Day) in the [W3C Design Tokens format](https://www.designtokens.org/tr/drafts/format/), plus the resolved `airframe-tokens.json`. For Figma variables, Style Dictionary, Terrazzo and scripts that draw. |
| `airframe-docs` | The docs-site look, for a Material for MkDocs or Zensical site: `airframe-docs.css` into `docs/stylesheets/`, and the suite strip and footer partials into `overrides/partials/`. Wiring is in [the docs sites](index.md#the-docs-sites). |
| `helpers` | `airframe/airframe.js`: the optional ES module with the markup helpers (`status`, `icon`, `meta`, `btn`, `avatar`, `obj`, `tag`) and the toast, confirm and drawer behaviours. No dependencies, no build step. |

### For coding agents

| Item | What it installs |
| --- | --- |
| `skill` | The Airframe skill, at `.claude/skills/airframe/` (Claude Code) and `.agents/skills/airframe/` (Codex): the rules, the classes and where each contract lives. |

### Component contracts

Each of these installs one component's contract as `airframe/components/<Name>.md`, next to the code. Each depends on `airframe` and on the components it is built from.

| Kind | Items |
| --- | --- |
| Foundations and cards | `button`, `status`, `card`, `avatar`, `object-chip` |
| Governance | `approval-card`, `question`, `decision-deck` |
| Controls and data | `composer`, `diff` |
| Fleet | `fleet-bay`, `stage-rail`, `heartbeat`, `activity-timeline`, `agent-row`, `agent-card`, `fleet-console` |
| Patterns | `page-header`, `empty-state`, `toast`, `dialog`, `drawer`. Toast, dialog and drawer also pull in `helpers`. |

### React

| Item | What it installs |
| --- | --- |
| `react` | `src/components/airframe/{Button,Status,Card,Icon}.tsx`: thin wrappers that only compose `af-` classes. A prototype; the consoles are vanilla JS. |

## How it is built

The source is [`registry.json`](https://github.com/Sean-Koval/agent-factory/blob/main/registry.json) at the repository root. `python3 scripts/airframe.py registry DIR` inlines each item's files into `DIR/<item>.json`, which this site serves under `/r/`. `python3 scripts/airframe.py check` validates the registry with the rest of Airframe.
