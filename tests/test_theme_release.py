"""Tests for scripts/theme_release.py. Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import theme_release as tr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

V1 = "# Changelog\n\nIntro.\n\n## theme-v1 · 2026-10-17\n\n- first\n"
V2 = "# Changelog\n\nIntro.\n\n## theme-v2 · 2026-11-01\n\n- `--af-brand` changed\n\n## theme-v1 · 2026-10-17\n\n- first\n"


class VersionTests(unittest.TestCase):
    def test_newest_and_notes(self):
        self.assertEqual(tr.newest(V2), ("theme-v2", 2))
        self.assertEqual(tr.notes(V2, "theme-v2"), "- `--af-brand` changed\n")
        self.assertEqual(tr.notes(V2, "theme-v1"), "- first\n")
        self.assertIsNone(tr.newest("# empty\n"))

    def test_order_and_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            tr.newest("## theme-v1\n\n## theme-v2\n")
        with self.assertRaises(ValueError):
            tr.newest("## theme-v2\n\n## theme-v2\n")
        with self.assertRaises(ValueError):
            tr.notes(V1, "theme-v9")

    def test_checked_in_changelog(self):
        text = (ROOT / tr.CHANGELOG).read_text()
        tag, _ = tr.newest(text)
        self.assertRegex(tag, r"^theme-v\d+$")
        self.assertTrue(tr.notes(text, tag).strip())


class CheckTests(unittest.TestCase):
    def test_theme_change_without_new_entry_fails(self):
        problems = tr.check("origin/main", V1, V1, ["theme/airframe.css"])
        self.assertEqual(len(problems), 1)
        self.assertIn("theme-v2", problems[0])

    def test_theme_change_with_new_entry_passes(self):
        self.assertEqual(tr.check("origin/main", V2, V1, ["theme/airframe-docs.css"]), [])

    def test_unrelated_change_passes_and_first_changelog_passes(self):
        self.assertEqual(tr.check("origin/main", V1, V1, ["docs/index.md", "theme/suite.css"]), [])
        self.assertEqual(tr.check("origin/main", V1, "", ["theme/airframe.css", tr.CHANGELOG]), [])

    def test_missing_or_broken_changelog_fails(self):
        self.assertTrue(tr.check("origin/main", "# none\n", V1, []))
        self.assertTrue(tr.check("origin/main", "## theme-v1\n## theme-v3\n", V1, []))


if __name__ == "__main__":
    unittest.main()
