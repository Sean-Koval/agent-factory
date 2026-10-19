#!/usr/bin/env python3
"""Build the roadmap include for docs/roadmap.md from GitHub issue state.

Reads roadmap.toml (repositories, phases matched to milestones, themes mapping issues),
fetches every issue of each public repository through the GitHub REST API and writes
generated/roadmap.md, which docs/roadmap.md pulls in with a snippet. The output is built
in CI and never committed.

    python3 scripts/roadmap.py                 # writes generated/roadmap.md
    python3 scripts/roadmap.py --strict        # CI: fail instead of writing a placeholder
    python3 scripts/roadmap.py --offline       # placeholder only, no network

A token is optional for public repositories; set GITHUB_TOKEN (or GH_TOKEN) to raise the
rate limit. Private repositories are skipped (named, not shown) unless --include-private
is passed, so the public site never lists their issues. REST only: no GraphQL.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tomllib
import urllib.error
import urllib.request
from urllib.parse import quote
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
PER_PAGE = 100
MAX_PAGES = 50


class FetchError(Exception):
    """A request failed for a reason other than "not found"."""


class NotFound(FetchError):
    """404: the repository is missing or private to this token."""


# A fetcher takes an API path ("/repos/o/r/issues?...") and returns decoded JSON.
Fetcher = Callable[[str], object]


def http_fetcher(token: str | None) -> Fetcher:
    def fetch(path: str) -> object:
        req = urllib.request.Request(API + path)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "agent-factory-roadmap")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise NotFound(path) from exc
            if exc.code == 403 and exc.headers.get("X-RateLimit-Remaining") != "0":
                # Forbidden without an exhausted rate limit: this token may not see the repo.
                raise NotFound(path) from exc
            raise FetchError(f"{path}: HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise FetchError(f"{path}: {exc}") from exc

    return fetch


# --- configuration --------------------------------------------------------------------------

REF = re.compile(r"^(?P<repo>[A-Za-z0-9_.-]+)#(?P<first>\d+)(?:-(?P<last>\d+))?$")


@dataclass
class Repo:
    key: str
    name: str
    slugs: list[str]
    epics: list[int] = field(default_factory=list)


@dataclass
class Theme:
    title: str
    refs: list[tuple[str, int]]
    label: str | None = None


@dataclass
class Phase:
    key: str
    title: str
    when: str
    milestone: str
    themes: list[Theme]
    done: str = ""  # what finishing the phase means, in one sentence


@dataclass
class Config:
    repos: list[Repo]
    phases: list[Phase]


def expand(ref: str, repo_keys: set[str]) -> list[tuple[str, int]]:
    m = REF.match(ref.strip())
    if not m:
        raise ValueError(f"bad issue reference {ref!r}; use 'repo#12' or 'repo#12-15'")
    repo = m["repo"]
    if repo not in repo_keys:
        raise ValueError(f"issue reference {ref!r} names unknown repo {repo!r}")
    first = int(m["first"])
    last = int(m["last"] or first)
    if last < first:
        raise ValueError(f"issue range {ref!r} runs backwards")
    return [(repo, n) for n in range(first, last + 1)]


def load_config(path: Path) -> Config:
    data = tomllib.loads(path.read_text())
    repos = [
        Repo(key=r["key"], name=r.get("name", r["key"]), slugs=list(r["slugs"]),
             epics=[int(n) for n in r.get("epics", [])])
        for r in data.get("repo", [])
    ]
    keys = {r.key for r in repos}
    if len(keys) != len(repos):
        raise ValueError("duplicate repo key in roadmap config")
    phases = []
    for p in data.get("phase", []):
        themes = []
        for t in p.get("theme", []):
            refs: list[tuple[str, int]] = []
            for ref in t.get("issues", []):
                for item in expand(ref, keys):
                    if item not in refs:
                        refs.append(item)
            themes.append(Theme(title=t["title"], refs=refs, label=t.get("label")))
        phases.append(Phase(key=p["key"], title=p.get("title", p["key"]), when=p.get("when", ""),
                            milestone=p.get("milestone", p["key"]), themes=themes, done=p.get("done", "")))
    return Config(repos=repos, phases=phases)


# --- fetching -------------------------------------------------------------------------------

@dataclass
class Issue:
    number: int
    title: str
    state: str  # open | closed
    reason: str | None  # completed | not_planned | reopened | None
    url: str
    milestone: str | None
    labels: list[str]


@dataclass
class RepoState:
    repo: Repo
    slug: str | None = None
    html_url: str | None = None
    status: str = "ok"  # ok | private | unavailable | error
    detail: str = ""
    issues: dict[int, Issue] = field(default_factory=dict)


def fetch_issues(fetch: Fetcher, slug: str) -> dict[int, Issue]:
    """Every issue (pull requests excluded), paging by number rather than Link headers."""
    out: dict[int, Issue] = {}
    for page in range(1, MAX_PAGES + 1):
        batch = fetch(f"/repos/{slug}/issues?state=all&per_page={PER_PAGE}&page={page}")
        if not isinstance(batch, list):
            raise FetchError(f"{slug}: unexpected issues payload")
        for item in batch:
            if "pull_request" in item:
                continue
            out[item["number"]] = Issue(
                number=item["number"],
                title=item["title"],
                state=item["state"],
                reason=item.get("state_reason"),
                url=item["html_url"],
                milestone=(item.get("milestone") or {}).get("title"),
                labels=[lb["name"] for lb in item.get("labels", [])],
            )
        if len(batch) < PER_PAGE:
            return out
    raise FetchError(f"{slug}: more than {MAX_PAGES * PER_PAGE} issues")


def fetch_repo(fetch: Fetcher, repo: Repo, include_private: bool) -> RepoState:
    state = RepoState(repo=repo)
    for slug in repo.slugs:
        try:
            meta = fetch(f"/repos/{slug}")
        except NotFound:
            continue
        except FetchError as exc:
            state.status, state.detail = "error", str(exc)
            return state
        assert isinstance(meta, dict)
        state.slug = meta.get("full_name", slug)
        state.html_url = meta.get("html_url", f"https://github.com/{slug}")
        if meta.get("private") and not include_private:
            state.status = "private"
            return state
        try:
            state.issues = fetch_issues(fetch, state.slug)
        except FetchError as exc:
            state.status, state.detail = "error", str(exc)
        return state
    state.status = "unavailable"
    state.detail = "private or not found"
    return state


# --- rendering ------------------------------------------------------------------------------

def md_text(text: str) -> str:
    """Escape an issue title for inline Markdown; keep `code` spans as written."""
    parts = text.split("`")
    if len(parts) % 2 == 0:  # unbalanced backticks: no code spans, escape them all
        parts = [text]
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:  # prose; code spans (odd parts) are literal already
            part = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            part = re.sub(r"([\\*_\[\]|`])", r"\\\1", part)
        out.append(part)
    return "`".join(out)


def phase_of(issue: Issue, phases: list[Phase]) -> Phase | None:
    if not issue.milestone:
        return None
    for phase in phases:
        if issue.milestone == phase.milestone or issue.milestone.startswith(phase.milestone + " "):
            return phase
    return None


def badge(issue: Issue) -> str:
    """A closed issue gets a check mark, a dropped one a dash; an open one is plain (the state is not a status)."""
    if issue.state == "open":
        return '<span class="af-rm-state af-rm-open" aria-label="open"></span>'
    if issue.reason == "not_planned":
        return '<span class="af-rm-state af-rm-dropped" aria-label="dropped">–</span>'
    return '<span class="af-rm-state af-rm-closed" aria-label="closed">✓</span>'


def item_line(repo_key: str, issue: Issue, note: str = "") -> str:
    suffix = f" <small>{note}</small>" if note else ""
    title = md_text(issue.title)
    if issue.state != "open" and issue.reason == "not_planned":
        title = f"<s>{title}</s>"
    return f"- {badge(issue)} [{repo_key}#{issue.number}]({issue.url}) {title}{suffix}"


def theme_row(title: str, closed: int, filed: int, items: list[str]) -> list[str]:
    """One row per theme: its name, the count in the house style ("18 of 21") and a 4 px greyscale bar.
    The row is the summary of a <details> holding the issue list, closed by default."""
    pct = round(100 * closed / filed) if filed else 0
    row = (f'<span class="af-rm-theme__name">{md_text(title)}</span>'
           f'<span class="af-rm-count">{closed} of {filed} closed</span>'
           f'<span class="af-rm-bar" role="img" aria-label="{pct} percent closed" style="--af-rm-pct: {pct}%"></span>')
    if not items:
        return [f'<p class="af-rm-theme">{row}</p>', ""]
    return ['<details class="af-rm-theme" markdown>', f"<summary>{row}</summary>", ""] + items + ["", "</details>", ""]


def folded(summary: str, items: list[str]) -> list[str]:
    """An issue list closed by default; the count above it is what a reader sees first."""
    return ['<details class="af-rm-issues" markdown>', f"<summary>{summary}</summary>", ""] + items + ["", "</details>"]


def count(issues: list[Issue]) -> tuple[int, int]:
    return sum(1 for i in issues if i.state == "closed"), len(issues)


def milestone_work(s: RepoState, phase: Phase, phases: list[Phase]) -> list[Issue]:
    """A repository's issues in a phase's milestone, epics excluded: an epic tracks the work, it isn't any."""
    return [i for i in s.issues.values() if phase_of(i, phases) is phase and i.number not in s.repo.epics]


def plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def render(cfg: Config, states: list[RepoState], now: dt.datetime) -> tuple[str, list[str]]:
    """Return the Markdown include and a list of warnings."""
    warnings: list[str] = []
    by_key = {s.repo.key: s for s in states}
    shown = [s for s in states if s.status == "ok"]
    lines: list[str] = []
    stamp = now.strftime("%Y-%m-%d %H:%M UTC")

    # Progress grid: phases x repositories.
    lines.append("## Progress")
    lines.append("")
    lines.append('<div class="af-rm-progress" markdown>')
    lines.append("")
    done = any(p.done for p in cfg.phases)
    header = ["Phase"] + (["Done when"] if done else []) + [s.repo.name for s in shown] + ["All"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * (2 if done else 1) + ["---:"] * (len(header) - (2 if done else 1))) + " |")
    for phase in cfg.phases:
        row = [f"[{phase.title}](#{anchor(phase.title)})<br><small>{md_text(phase.when)}</small>"]
        if done:
            row.append(md_text(phase.done))
        total_c = total_n = 0
        for s in shown:
            issues = milestone_work(s, phase, cfg.phases)
            c, n = count(issues)
            total_c, total_n = total_c + c, total_n + n
            row.append(cell(c, n, milestone_url(s, issues)))
        row.append(cell(total_c, total_n, None))
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    hidden = [s for s in states if s.status != "ok"]
    if hidden:
        notes = []
        for s in hidden:
            why = {"private": "private repository, not shown",
                   "unavailable": "private or not found, not shown",
                   "error": f"could not be read ({s.detail})"}[s.status]
            notes.append(f"{s.repo.name}: {why}")
        lines.append('<p class="af-rm-note">' + md_text("; ".join(notes)) + ".</p>")
        lines.append("")

    # Epics.
    epic_lines = []
    for s in shown:
        for n in s.repo.epics:
            issue = s.issues.get(n)
            if issue:
                epic_lines.append(item_line(s.repo.key, issue))
            else:
                warnings.append(f"{s.repo.key}#{n}: epic not found")
    for s in hidden:
        for n in s.repo.epics:
            epic_lines.append(f"- {s.repo.key}#{n} <small>(private repository)</small>")
    if epic_lines:
        lines.extend(folded(f"The {plural(len(epic_lines), 'epic')} that track this work", epic_lines))
        lines.append("")
    lines.append(f'<p class="af-rm-stamp">Built {stamp} from GitHub issue state. '
                 "Counts are closed of filed issues per milestone; epics and pull requests are not counted.</p>")
    lines.append("")

    # Themes per phase.
    placed: set[tuple[str, int]] = set()
    for phase in cfg.phases:
        phase_issues = [i for s in shown for i in milestone_work(s, phase, cfg.phases)]
        c, n = count(phase_issues)
        lines.append(f"## {phase.title}")
        lines.append("")
        lines.append(f'<p class="af-rm-phase">{md_text(phase.when)} · {c} of {n} closed</p>')
        lines.append("")
        for theme in phase.themes:
            refs = list(theme.refs)
            if theme.label:
                for s in shown:
                    for i in sorted(s.issues.values(), key=lambda i: i.number):
                        if theme.label in i.labels and phase_of(i, cfg.phases) is phase \
                                and (s.repo.key, i.number) not in refs:
                            refs.append((s.repo.key, i.number))
            items: list[str] = []
            found: list[Issue] = []
            private_refs: list[str] = []
            for key, num in refs:
                placed.add((key, num))
                st = by_key[key]
                if st.status != "ok":
                    private_refs.append(f"{key}#{num}")
                    continue
                issue = st.issues.get(num)
                if issue is None:
                    warnings.append(f"{key}#{num} ({theme.title}): not an issue in {st.slug}")
                    continue
                found.append(issue)
                note = ""
                other = phase_of(issue, cfg.phases)
                if other is not phase:
                    note = f"({other.key})" if other else "(no milestone)"
                items.append(item_line(key, issue, note))
            tc, tn = count(found)
            if found or not private_refs:
                if private_refs:
                    items.append(f"- <small>Also in private repositories: {', '.join(private_refs)}</small>")
                lines.extend(theme_row(theme.title, tc, tn, items))
            else:  # only private issues: say so rather than "0 of 0 closed / No issues yet"
                lines.append(f'<p class="af-rm-theme"><span class="af-rm-theme__name">{md_text(theme.title)}</span>'
                             f'<span class="af-rm-count">{plural(len(private_refs), "issue")} in private repositories: '
                             f"{', '.join(private_refs)}</span></p>")
                lines.append("")

    # Unsorted: open issues no theme lists, epics excepted.
    lines.append("## Unsorted")
    lines.append("")
    unsorted = []
    for s in shown:
        for issue in sorted(s.issues.values(), key=lambda i: i.number):
            if issue.state != "open" or issue.number in s.repo.epics:
                continue
            if (s.repo.key, issue.number) in placed:
                continue
            ph = phase_of(issue, cfg.phases)
            note = f"({ph.key})" if ph else f"({issue.milestone})" if issue.milestone else "(no milestone)"
            unsorted.append(item_line(s.repo.key, issue, note))
    if unsorted:
        lines.append("Open issues that `roadmap.toml` does not place in a theme yet.")
        lines.append("")
        lines.extend(folded(plural(len(unsorted), "open issue"), unsorted))
    else:
        lines.append("Every open issue is placed in a theme.")
    lines.append("")
    return "\n".join(lines), warnings


def anchor(title: str) -> str:
    """Approximate the toc extension's slug for a heading."""
    s = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"[\s]+", "-", s.strip())


def cell(closed: int, filed: int, url: str | None) -> str:
    if not filed:
        return "–"
    text = f"{closed} of {filed}"
    return f"[{text}]({url})" if url else text


def milestone_url(s: RepoState, issues: list[Issue]) -> str | None:
    titles = {i.milestone for i in issues if i.milestone}
    if len(titles) != 1 or not s.html_url:
        return None
    return f"{s.html_url}/issues?q=" + quote(f'is:issue milestone:"{titles.pop()}"')


PLACEHOLDER = """<p class="af-rm-note">The roadmap data was not built for this copy of the site.
It is generated from GitHub issue state when the site is published; run
<code>python3 scripts/roadmap.py</code> to build it locally.</p>

## Unsorted

Not built.
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", type=Path, default=ROOT / "roadmap.toml")
    ap.add_argument("--out", type=Path, default=ROOT / "generated" / "roadmap.md")
    ap.add_argument("--strict", action="store_true",
                    help="fail when a public repository cannot be read instead of degrading")
    ap.add_argument("--offline", action="store_true", help="write the placeholder only")
    ap.add_argument("--include-private", action="store_true",
                    help="show private repositories the token can read (never for the public site)")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.offline:
        args.out.write_text(PLACEHOLDER)
        print(f"roadmap: wrote placeholder to {args.out}")
        return 0

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or None
    fetch = http_fetcher(token)
    states = [fetch_repo(fetch, r, args.include_private) for r in cfg.repos]
    errors = [s for s in states if s.status == "error"]
    for s in states:
        if s.status != "ok":
            print(f"roadmap: {s.repo.key}: {s.status} {s.detail}".rstrip(), file=sys.stderr)
    if errors and all(s.status != "ok" for s in states):
        if args.strict:
            return 1
        args.out.write_text(PLACEHOLDER)
        print(f"roadmap: GitHub unreachable; wrote placeholder to {args.out}", file=sys.stderr)
        return 0

    text, warnings = render(cfg, states, dt.datetime.now(dt.timezone.utc))
    for w in warnings:
        # A GitHub Actions annotation in CI, a plain line elsewhere.
        prefix = "::warning::" if os.environ.get("GITHUB_ACTIONS") else "roadmap: warning: "
        print(f"{prefix}{w}", file=sys.stderr)
    if args.strict and errors:
        return 1
    args.out.write_text(text)
    print(f"roadmap: wrote {args.out} ({sum(len(s.issues) for s in states)} issues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
