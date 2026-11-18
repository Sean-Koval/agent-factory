# Compatibility

Which versions of the tools are meant to run together, and which Airframe theme each one vendors. Read it before you install more than one tool. How a version is made is on [Releasing](index.md).

## Suite 1.0

Suite 1.0 is hangar, Tower and flightdeck, each at a tagged version. The table is the current candidate. It becomes 1.0 when every row has a tag made with the [checklist](index.md#the-checklist).

| Component | Last tag | 1.0 candidate | Airframe on main |
| --- | --- | --- | --- |
| hangar | v0.2.0 | v1.0.0-rc.1, prepared in a PR | theme-v16 |
| Tower | none; v0.1.0 is ready | v1.0.0-rc.1, prepared in a PR | theme-v16 |
| flightdeck | none; v0.1.0 is ready | v1.0.0-rc.1, prepared in a PR | theme-v16 |

Checked on 18 November 2026 against each repo's tags and `main`. A prepared candidate has its version and changelog cut in an open PR and no tag yet. Tower's and flightdeck's v0.1.0 tags can still go on their older commits first.

ai-dlc (v0.4.0), Spaceport and the team harness are outside the 1.0 set.

### The Airframe theme {#the-airframe-theme}

All three tools vendor theme-v16 on `main`. theme-v17, released on 18 November, changes the docs-site layer, and no tool has synced it yet. Each candidate ships the theme on `main` when its rc PR merges. So a theme-v17 sync goes in before the rc PRs, in all three tools, or in none.

Each tool vendors its own copy of Airframe. Mixed themes still work, because token names only ever gain aliases. A suite release should still ship one theme throughout.

## How the parts depend on each other

- **Tower and hangar** talk over hangar's API and its webhook events.
- **flightdeck** reads hangar's run outbox in the `flightdeck.parquet/v1` tables.

A change to either contract is a breaking change. Its changelog names the versions on the other side that still work. The contracts themselves are indexed on [Contracts](../architecture/contracts.md).
