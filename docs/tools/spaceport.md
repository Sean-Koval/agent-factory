<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-spaceport); }</style>

<span class="af-eyebrow">Agent factory · Capability</span>

# Spaceport

Reviewed data products that agents query through four MCP tools. Frozen.

| | |
| --- | --- |
| Owns | A catalog, a publisher where the author is never the publisher, immutable versions, tenant-scoped execution, REST and four MCP tools (`search_products`, `describe_product`, `query_product`, `get_result`). |
| Does not own | Policy decisions for agents. Later it will ask Tower. |
| Used by | Agents through an environment's MCP binding, and data owners. |
| Status | **Frozen** since 2026-10-16 (spaceport#10): security fixes and cleanup only, no new connectors, live sources or deployment. The cleanup issues (naming, licensing, docs index: spaceport#11–#13, #15) closed by Oct 17. Asking Tower's decision point (spaceport#14) waits in the backlog. |
| Docs site | None: a README only, in a private repository (Sean-Koval/spaceport). |
