# Releasing a suite component

This page is for the person who tags a release of hangar, Tower or flightdeck. Every component follows the same checklist, so a version means the same thing everywhere. Which versions make up a suite release is on [Compatibility](compatibility.md).

## Versions

A release is a `vX.Y.Z` tag on `main`. Before 1.0, a minor bump may break things, and its changelog says how. Each repo keeps its version in one place:

| Component | Version source | Prints it |
| --- | --- | --- |
| hangar | `pyproject.toml` | The image label `org.opencontainers.image.version` |
| Tower | `server/aw/__init__.py` | `GET /api/health` (`version`) |
| flightdeck | `pyproject.toml` and `src/flightdeck/__init__.py` | `flightdeck version` |

Each repo has a `CHANGELOG.md` whose newest section is `## Unreleased`. Every merged change that a user would notice adds a line there.

## The checklist

Copy it into the release's Jira ticket and tick each line.

1. **Changelog.** Rename `## Unreleased` to `## vX.Y.Z: <a name>`, start a new empty `## Unreleased`, and bump the version source in the same PR.
2. **Green CI on that commit.** Merge the PR, then wait for every required check to pass on the merge commit in `main`. Don't tag a commit whose checks were skipped.
3. **Tag it.** Run `git tag -a vX.Y.Z -m vX.Y.Z <sha>` and push the tag. The release workflow refuses a tag that doesn't match the version source.
4. **GitHub release.** The release workflow publishes it, with the changelog section as its notes. Check that it exists and reads well.
5. **Docs version.** The docs site names the release on its front page or release notes. hangar also adds a row to `docs/releases/README.md`.
6. **Deployed sha matches the tag.** After the deploy, compare the running image's commit or digest with the tag. A mismatch means the deploy is not the release.
7. **Compatibility.** Update the row on [Compatibility](compatibility.md) in agent-factory, with the Airframe theme the release vendors.

## Repository settings

Every repo has "Automatically delete head branches" turned on. A stacked PR then retargets to `main` when its base merges, instead of merging into a dead branch.
