# Compatibility

This page is for anyone who installs more than one tool in the suite. It lists which versions are meant to run together, and which Airframe theme each one vendors. How a version is made is on [Releasing](index.md).

## Suite 1.0

Suite 1.0 is hangar, Tower and flightdeck, each at a tagged version. The table is the current candidate. It becomes 1.0 when every row has a tag made with the [checklist](index.md#the-checklist).

| Component | Version | Airframe | Status |
| --- | --- | --- | --- |
| hangar | v0.2.0 | theme-v15 | Tagged |
| Tower | v0.1.0 | theme-v15 | Tag pending |
| flightdeck | v0.1.0 | theme-v15 | Tag pending |

ai-dlc (v0.4.0), Spaceport and the team harness are outside the 1.0 set.

## How the parts depend on each other

Tower talks to hangar over hangar's API and its webhook events. flightdeck reads hangar's run outbox in the `flightdeck.parquet/v1` tables. A change to either contract is a breaking change. Its changelog names the versions on the other side that still work.

Each tool vendors its own copy of Airframe. Mixed themes still work, because token names only ever gain aliases. A suite release should still ship one theme throughout.
