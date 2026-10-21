<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-flightdeck); }</style>

<span class="af-eyebrow">Agent factory · Judge</span>

# flightdeck

Judges harness changes with paired statistics and behavior specs over every run.

<figure class="af-figure af-figure--lead">
<a href="../assets/captures/flightdeck-verdict.png"><img src="../assets/captures/flightdeck-verdict-verdict.png#only-dark" alt="flightdeck's report as a GitHub pull-request comment: the verdict, candidate is better than control on resolved (+21.2 pp), the rule and the outcome table" width="790" height="520"></a>
<a href="../assets/captures/flightdeck-verdict-day.png"><img src="../assets/captures/flightdeck-verdict-day-verdict.png#only-light" alt="flightdeck's report as a GitHub pull-request comment: the verdict, candidate is better than control on resolved (+21.2 pp), the rule and the outcome table" width="790" height="520"></a>
<figcaption>The verdict on the harness PR: candidate beats control on resolved, with the interval and the outcome of both variants.</figcaption>
</figure>

| | |
| --- | --- |
| Owns | The Parquet data plane, paired statistics, behavior specs, trial sampling, experiment reports. |
| Does not own | Sandboxes, credentials or provider code. It reads hangar's exports and the outbox, never its database. |
| Entry points | The `flightdeck` CLI; reports posted as GitHub comments; a nightly `check run`. |
| Used by | The harness owner and lead deciding promotions, engineers reading reports on harness PRs, nightly CI. |
| Status | The data plane, statistics, reports and the spec language are shipped; the nightly runner and one real decision are next. See [P3 on the roadmap](../roadmap.md#p3-flightdeck-v0). |

[Docs site](https://sean-koval.github.io/flightdeck/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/flightdeck){ .md-button }
