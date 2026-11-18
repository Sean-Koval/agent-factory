# Releasing a suite component

How to tag a release of hangar, Tower or flightdeck. Every component follows the same checklist, so a version means the same thing everywhere. Which versions make up a suite release is on [Compatibility](compatibility.md).

## Versions

A release is a `vX.Y.Z` tag on `main`. Before 1.0, a minor bump may break things, and its changelog says how.

A release candidate is a `vX.Y.Z-rc.N` tag. It follows the same checklist, and the release workflow marks its GitHub release as a pre-release. Spell the version source the way the tag does: tag `v1.0.0-rc.1` needs `1.0.0-rc.1`, not `1.0.0rc1`.

Each repo keeps its version in one place and prints it in one place:

- **hangar** keeps it in `pyproject.toml`. The image label `org.opencontainers.image.version` prints it.
- **Tower** keeps it in `server/aw/__init__.py`. `GET /api/health` prints it as `version`.
- **flightdeck** keeps it in `pyproject.toml` and `src/flightdeck/__init__.py`. `flightdeck version` prints it.

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

## Suite 1.0

Suite 1.0 ships as two rounds of tags, made in the same order in each repo: hangar, Tower, then flightdeck.

1. **The candidate.** Each tool tags `v1.0.0-rc.1` from a PR that cuts its changelog. Merge those PRs last, after the rest of the queue, so the cut carries everything.
2. **The final.** Once the candidate has run in production and every exit criterion holds, each tool tags `v1.0.0`. It needs its own `## v1.0.0` changelog section, because the check never reads the candidate's section for a final tag.

A fix found on the candidate goes out as `-rc.2`, not as a patch to the tag. The exit criteria and their evidence are tracked on the 1.0 readiness page.

## Repository settings

Two settings make the checklist binding, and no file in a repo can make either.

- **Delete head branches.** Every repo has "Automatically delete head branches" turned on. A stacked PR then retargets to `main` when its base merges, instead of merging into a dead branch.
- **A tag ruleset on `v*`.** It blocks creating, updating and deleting release tags. Its sole bypass is a deploy key kept on the owner's machine. Agents push as the owner's account, so a bypass for the owner or the admin role stops no agent.
