<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-spaceport); }</style>

<span class="af-eyebrow">Agent factory · Capability</span>

# Spaceport

Reviewed data products that agents query through four MCP tools. Frozen.

!!! note "Status"
    Frozen since 2026-10-16: security fixes and cleanup only, with no new connectors, sources or deployment.

## What Spaceport owns

| | |
| --- | --- |
| Owns | A catalog, a publisher where the author is never the publisher, immutable versions, tenant-scoped execution. |
| Does not own | Policy decisions for agents. Later it will ask Tower. |
| Entry points | REST and four MCP tools. |
| Used by | Agents through an environment's MCP binding, and data owners. |
| Docs site | None: a README only, in a private repository (Sean-Koval/spaceport). |

## The four MCP tools

An agent sees Spaceport as four tools with typed results:

- `search_products`
- `describe_product`
- `query_product`
- `get_result`

## Works with

- **[hangar](hangar.md).** An environment binds Spaceport's MCP server into the sandboxes claimed from it.
- **[Tower](workspace.md).** Asking Tower's decision point waits in the backlog.
- **[Contracts](../architecture/contracts.md).** The four tools are one row there, on main and frozen.

[How it fits](../how-it-fits.md) follows one ticket through all four planes.
