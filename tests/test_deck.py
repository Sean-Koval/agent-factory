"""The deck source (deck/src.html): footers carry takeaways, screens show crops, nothing names a theme version.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import captures  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "deck" / "src.html").read_text()
SLIDES = re.findall(r'<section class="slide[^"]*"[^>]*>(.*?)</section>', SRC, re.S)


class DeckTests(unittest.TestCase):
    def test_screen_slides_show_a_named_crop(self):
        crops = {f"{base}-{crop}" for base, cs in captures.CROPS.items() for crop in cs}
        shown = re.findall(r'src="captures/([\w-]+)\.png"', SRC)
        self.assertTrue(shown)
        for name in shown:
            self.assertIn(name, crops, f"the deck shows {name}, a full window, not the subject")

    def test_footers_are_takeaways_not_build_notes(self):
        for slide in SLIDES:
            foot = re.search(r'<div class="foot"><span>(.*?)</span>', slide).group(1)
            self.assertNotIn("captures.py", foot)
            self.assertNotIn("scripts/", foot)
            if 'class="screen-grid"' in slide or 'class="readouts"' in slide:
                self.assertGreaterEqual(len(foot.split()), 6, f"a takeaway, not a label: {foot}")
        self.assertNotIn("1440 × 900", SRC, "a capture's size is provenance, not a caption")

    def test_no_stale_version_or_date(self):
        self.assertNotRegex(SRC, r"theme-v\d+")
        self.assertNotRegex(SRC, r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}")

    def test_screen_slides_are_short(self):
        for slide in SLIDES:
            if 'class="screen-grid"' not in slide:
                continue
            lede = re.search(r'<p class="lede">(.*?)</p>', slide, re.S).group(1)
            self.assertLessEqual(len(re.sub(r"<[^>]+>", "", lede).split()), 30, lede)
            self.assertLessEqual(len(re.findall(r"<li>", slide)), 2, "two bullets at most on a screen slide")

    def test_footer_reads_at_aa(self):
        """The title slide's URL and every footer are fg-muted (>= 4.5:1), never fg-dim."""
        foot = re.search(r"\.foot \{[^}]*\}", SRC).group(0)
        self.assertIn("var(--af-fg-muted)", foot)
        self.assertNotIn("fg-dim", foot)
