<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-flightdeck); }</style>

<span class="af-eyebrow">Judge plane</span>

# flightdeck

Reads every run from a Parquet data plane and answers whether a change made agents better.

| | |
| --- | --- |
| Owns | `flightdeck.parquet/v1`, paired statistics (Wilson intervals, pass^k, paired bootstrap, cost per resolved task), behavior specs and nightly ADR checks, task sets and sealed holdouts, experiment submission and reports. |
| Does not own | Sandboxes, credentials or provider code. It never reads hangar's database; it reads exports and the outbox. |
| Entry points | The `flightdeck` CLI; reports posted as GitHub comments; a nightly `check run`. |
| Used by | The harness owner and lead deciding promotions, engineers reading reports on harness PRs, nightly CI. |

[Docs site](https://sean-koval.github.io/flightdeck/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/flightdeck){ .md-button }
