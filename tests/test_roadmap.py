"""Tests for scripts/roadmap.py. Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import roadmap  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOW = dt.datetime(2026, 10, 17, 12, 0, tzinfo=dt.timezone.utc)

CONFIG = """
[[repo]]
key = "alpha"
name = "Alpha"
slugs = ["o/alpha-new", "o/alpha"]
epics = [1]

[[repo]]
key = "secret"
slugs = ["o/secret"]
epics = [3]

[[phase]]
key = "P1"
title = "P1 · First"
when = "weeks 1-2"
milestone = "P1"

[[phase.theme]]
title = "Core"
issues = ["alpha#2-4", "secret#5"]

[[phase]]
key = "Backlog"
title = "Backlog"
milestone = "Backlog"

[[phase.theme]]
title = "Spikes"
label = "type:spike"
"""


def issue(n, state="open", milestone=None, labels=(), title=None, reason=None, pr=False):
    item = {
        "number": n, "title": title or f"Issue {n}", "state": state, "state_reason": reason,
        "html_url": f"https://github.com/o/alpha/issues/{n}",
        "milestone": {"title": milestone} if milestone else None,
        "labels": [{"name": lb} for lb in labels],
    }
    if pr:
        item["pull_request"] = {"url": "x"}
    return item


class FakeGitHub:
    """Answers REST paths from a table; unknown repositories are 404."""

    def __init__(self, repos):
        self.repos = repos  # slug -> {"private": bool, "issues": [...]}
        self.calls = []

    def __call__(self, path):
        self.calls.append(path)
        url = urlparse(path)
        parts = url.path.strip("/").split("/")
        slug = "/".join(parts[1:3])
        if slug not in self.repos:
            raise roadmap.NotFound(path)
        repo = self.repos[slug]
        if len(parts) == 3:
            return {"full_name": slug, "private": repo["private"], "html_url": f"https://github.com/{slug}"}
        q = parse_qs(url.query)
        page, per = int(q["page"][0]), int(q["per_page"][0])
        return repo["issues"][(page - 1) * per: page * per]


def load(text=CONFIG):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "roadmap.toml"
        p.write_text(text)
        return roadmap.load_config(p)


class ConfigTests(unittest.TestCase):
    def test_ranges_expand_and_dedupe(self):
        self.assertEqual(roadmap.expand("alpha#2-4", {"alpha"}), [("alpha", 2), ("alpha", 3), ("alpha", 4)])
        cfg = load(CONFIG.replace('"alpha#2-4", "secret#5"', '"alpha#2-3", "alpha#3"'))
        self.assertEqual(cfg.phases[0].themes[0].refs, [("alpha", 2), ("alpha", 3)])

    def test_bad_references_fail_loudly(self):
        for bad in ["beta#1", "alpha#5-2", "alpha 4"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                roadmap.expand(bad, {"alpha"})

    def test_checked_in_config_loads(self):
        cfg = roadmap.load_config(ROOT / "roadmap.toml")
        self.assertEqual([p.key for p in cfg.phases], ["P1", "P2", "P3", "P4", "Backlog"])
        self.assertIn("workspace", {r.key for r in cfg.repos})


class FetchTests(unittest.TestCase):
    def test_slug_fallback_pagination_and_pr_filter(self):
        issues = [issue(n, milestone="P1 First (wk 1-2)") for n in range(1, 151)] + [issue(151, pr=True)]
        gh = FakeGitHub({"o/alpha": {"private": False, "issues": issues}})
        repo = roadmap.Repo(key="alpha", name="Alpha", slugs=["o/alpha-new", "o/alpha"])
        st = roadmap.fetch_repo(gh, repo, include_private=False)
        self.assertEqual(st.status, "ok")
        self.assertEqual(st.slug, "o/alpha")
        self.assertEqual(len(st.issues), 150)
        self.assertNotIn(151, st.issues)
        self.assertTrue(any("page=2" in c for c in gh.calls))

    def test_private_repo_skipped_unless_asked(self):
        gh = FakeGitHub({"o/secret": {"private": True, "issues": [issue(5)]}})
        repo = roadmap.Repo(key="secret", name="secret", slugs=["o/secret"])
        self.assertEqual(roadmap.fetch_repo(gh, repo, include_private=False).status, "private")
        self.assertFalse(any("/issues" in c for c in gh.calls))
        self.assertEqual(roadmap.fetch_repo(gh, repo, include_private=True).status, "ok")

    def test_missing_repo_is_unavailable_and_errors_are_reported(self):
        repo = roadmap.Repo(key="x", name="x", slugs=["o/none"])
        self.assertEqual(roadmap.fetch_repo(FakeGitHub({}), repo, False).status, "unavailable")

        def broken(path):
            raise roadmap.FetchError("HTTP 500")

        st = roadmap.fetch_repo(broken, repo, False)
        self.assertEqual((st.status, st.detail), ("error", "HTTP 500"))


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load()
        alpha = [
            issue(1, milestone="P1 First (wk 1-2)", title="Epic"),
            issue(2, "closed", "P1 First (wk 1-2)"),
            issue(3, milestone="P1 First (wk 1-2)", title="Use `a <b>` and a_b|c"),
            issue(4, "closed", "Backlog", reason="not_planned"),
            issue(6, milestone="Backlog", labels=["type:spike"], title="Spike it"),
            issue(7, milestone="P1 First (wk 1-2)", title="Forgotten"),
            issue(8, "closed", "P1 First (wk 1-2)", title="Closed and unmapped"),
            issue(9, title="No milestone"),
        ]
        gh = FakeGitHub({"o/alpha": {"private": False, "issues": alpha},
                         "o/secret": {"private": True, "issues": [issue(5)]}})
        self.states = [roadmap.fetch_repo(gh, r, False) for r in self.cfg.repos]
        self.text, self.warnings = roadmap.render(self.cfg, self.states, NOW)

    def section(self, heading):
        """A phase ("## P1") or a theme ("### Core", found by its row's name span)."""
        if heading.startswith("### "):
            start = self.text.index(f'af-rm-theme__name">{heading[4:]}<')
            start = self.text.rfind("\n", 0, self.text.rfind("\n", 0, start)) + 1  # the <details> or <p> line
            nxt = [i for i in (self.text.find("\n<details class=\"af-rm-theme\"", start + 1),
                                self.text.find("\n<p class=\"af-rm-theme\"", start + 1),
                                self.text.find("\n## ", start + 1)) if i > 0]
            return self.text[start: min(nxt) if nxt else None]
        start = self.text.index(heading)
        end = self.text.find("\n## ", start + 1)
        return self.text[start: end if end > 0 else None]

    def test_counts_match_milestones(self):
        # P1 milestone: issues 2, 3, 7, 8 (epic 1 excluded) -> 2 closed of 4. Backlog: 4 and 6 -> 1 of 2.
        row = next(line for line in self.text.splitlines() if line.startswith("| [P1"))
        self.assertIn("2 of 4", row)
        self.assertNotIn(" / ", row)
        self.assertIn("<small>weeks 1-2</small>", row, "the phase's weeks sit under its name")

    def test_done_when_is_a_column_when_a_phase_says_it(self):
        cfg = load(CONFIG.replace('milestone = "P1"\n', 'milestone = "P1"\ndone = "Two engineers use it."\n'))
        text, _ = roadmap.render(cfg, self.states, NOW)
        head = next(line for line in text.splitlines() if line.startswith("| Phase"))
        self.assertEqual(head.split(" | ")[1], "Done when")
        self.assertIn("| Two engineers use it. |", text)
        self.assertNotIn("Done when", self.text, "no column when no phase has a sentence")
        self.assertIn("2 of 4 closed", self.section("## P1"))
        self.assertIn("1 of 2 closed", self.section("## Backlog"))
        self.assertIn("alpha#1]", self.section("## Progress"))  # still listed, folded under the table, not counted

    def test_theme_rows_carry_a_bar_and_fold_their_issues(self):
        core = self.section("### Core")
        self.assertIn('class="af-rm-bar"', core)
        self.assertIn("--af-rm-pct: 67%", core)  # 2 of 3 closed
        self.assertIn('<details class="af-rm-theme" markdown>', core)
        self.assertLess(core.index("af-rm-bar"), core.index("</summary>"), "the name, count and bar are the row that opens the list")
        self.assertIn('aria-label="closed">✓<', core)
        self.assertNotIn(">open<", core)  # an open issue is plain, not a placard
        self.assertNotIn(" / ", self.text)

    def test_unsorted_lists_every_unplaced_open_issue(self):
        unsorted = self.section("## Unsorted")
        self.assertIn("alpha#7", unsorted)
        self.assertIn("alpha#9", unsorted)
        self.assertIn("(no milestone)", unsorted)
        for placed in ["alpha#1", "alpha#3", "alpha#6", "alpha#8"]:  # epic, theme, label, closed
            self.assertNotIn(placed + "]", unsorted)

    def test_label_theme_and_out_of_phase_notes(self):
        self.assertIn("alpha#6", self.section("### Spikes"))
        core = self.section("### Core")
        self.assertIn("dropped", core)  # alpha#4 closed as not planned
        self.assertIn("(Backlog)", core)  # alpha#4 sits in another phase

    def test_private_repo_named_but_not_listed(self):
        self.assertIn("secret: private repository, not shown", self.text)
        self.assertIn("Also in private repositories: secret#5", self.text)
        self.assertNotIn("Issue 5", self.text)
        self.assertNotIn("| secret", self.text.splitlines()[4])

    def test_theme_with_only_private_issues_says_so(self):
        cfg = load(CONFIG.replace('title = "Spikes"\nlabel = "type:spike"',
                                  'title = "Spikes"\nlabel = "type:spike"\n\n[[phase.theme]]\n'
                                  'title = "Hidden"\nissues = ["secret#5-6"]'))
        text, _ = roadmap.render(cfg, self.states, NOW)
        hidden = text[text.index('af-rm-theme__name">Hidden<'):text.index("## Unsorted")]
        self.assertIn("2 issues in private repositories", hidden)
        self.assertIn("in private repositories: secret#5, secret#6", hidden)
        self.assertNotIn("0 of 0 closed", hidden)
        self.assertNotIn("No issues yet", hidden)
        core = self.section("### Core")  # a mixed theme keeps its count and its private note
        self.assertIn("2 of 3 closed", core)
        self.assertIn("Also in private repositories: secret#5", core)

    def test_titles_are_escaped_outside_code(self):
        self.assertIn("Use `a <b>` and a\\_b\\|c", self.text)
        self.assertEqual(roadmap.md_text("x <y> `z"), "x &lt;y&gt; \\`z")

    def test_dangling_reference_warns(self):
        cfg = load(CONFIG.replace('"alpha#2-4"', '"alpha#2-4", "alpha#99"'))
        _, warnings = roadmap.render(cfg, self.states, NOW)
        self.assertTrue(any("alpha#99" in w for w in warnings))
        self.assertEqual(self.warnings, [])


class MainTests(unittest.TestCase):
    def test_offline_writes_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "gen" / "roadmap.md"
            self.assertEqual(roadmap.main(["--offline", "--out", str(out)]), 0)
            self.assertIn("scripts/roadmap.py", out.read_text())


if __name__ == "__main__":
    unittest.main()
