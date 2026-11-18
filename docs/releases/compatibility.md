# Compatibility

Which versions of the tools are meant to run together, and which Airframe theme each one vendors. Read it before you install more than one tool. How a version is made is on [Releasing](index.md).

## Suite 1.0

Suite 1.0 is hangar, Tower and flightdeck, each at a tagged version. The table is the current candidate. It becomes 1.0 when every row has a tag made with the [checklist](index.md#the-checklist).

| Component | Version | Airframe |
| --- | --- | --- |
| hangar | v0.2.0, tagged | theme-v15 |
| Tower | v0.1.0, tag pending | theme-v15 |
| flightdeck | v0.1.0, tag pending | theme-v15 |

Checked on 9 November 2026 against each repo's tags. A pending version has its changelog ready and no tag yet. The Airframe column is the theme the tag vendors, or `main` for a pending tag.

ai-dlc (v0.4.0), Spaceport and the team harness are outside the 1.0 set.

### The Airframe theme {#the-airframe-theme}

theme-v16 is out, and it changes only the Terminal bar. No tool has synced it yet, so the candidate is on theme-v15 throughout. A tool that syncs theme-v16 before its tag moves its row, and the others follow.

Each tool vendors its own copy of Airframe. Mixed themes still work, because token names only ever gain aliases. A suite release should still ship one theme throughout.

## How the parts depend on each other

- **Tower and hangar** talk over hangar's API and its webhook events.
- **flightdeck** reads hangar's run outbox in the `flightdeck.parquet/v1` tables.

A change to either contract is a breaking change. Its changelog names the versions on the other side that still work. The contracts themselves are indexed on [Contracts](../architecture/contracts.md).
