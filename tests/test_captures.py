"""The product captures and their named crops (scripts/captures.py). Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import captures  # noqa: E402

ROOT = captures.ROOT
OUT = captures.OUT


class CropTests(unittest.TestCase):
    def test_every_named_crop_is_cut_from_its_capture_and_listed(self):
        """A crop is derived, never drawn: it exists, has the box's size and is in captures.json."""
        from PIL import Image

        manifest = json.loads((OUT / "captures.json").read_text())
        for name, crops in captures.CROPS.items():
            self.assertTrue((OUT / f"{name}.png").exists(), f"{name}: full capture missing")
            for crop, ((x, y, w, h), shows) in crops.items():
                f = OUT / f"{name}-{crop}.png"
                self.assertTrue(f.exists(), f"{f.name}: run python3 scripts/captures.py --crops")
                with Image.open(f) as img:
                    self.assertEqual(img.width, w * captures.SCALE, f.name)
                    self.assertLessEqual(img.height, h * captures.SCALE, f.name)
                self.assertGreaterEqual(len(shows.split()), 8, f"{f.name}: say what the crop shows")
                self.assertEqual(manifest["crops"][f"{name}-{crop}"]["box"], [x, y, w, h], f.name)

    def test_pages_show_a_crop_and_link_the_full_capture(self):
        """Where a page or the README shows a product, it shows the subject at a size where its text reads."""
        for page in (ROOT / "docs" / "index.md", ROOT / "README.md"):
            text = page.read_text()
            shown = re.findall(r'src="(?:docs/)?assets/captures/([\w-]+)\.png"', text)
            self.assertTrue(shown, f"{page.name}: no product capture")
            names = {f"{base}-{crop}" for base, crops in captures.CROPS.items() for crop in crops}
            for name in shown:
                self.assertIn(name, names, f"{page.name} shows {name}, which is not a named crop")

    def test_the_hero_crop_keeps_the_product_text_legible(self):
        """The home hero is about 600 px wide at 1440: a 1296 px crop lands 13 px labels at 6 px, 20 px headlines at 9 px."""
        (x, y, w, h), _ = captures.CROPS["hangar-fleet"]["needs-you"]
        self.assertLessEqual(w, 1300)
        self.assertLessEqual(h / w, 0.4, "the hero crop is wide: the tile row and the detail panel, not the empty canvas")

    def test_readme_opens_with_the_problem_and_a_picture(self):
        readme = (ROOT / "README.md").read_text()
        first = readme.split("## ", 1)[0]
        self.assertIn("**Hand work to cloud coding agents and keep every change reviewable.**", first)
        self.assertIn("slide-planes-dark.png", first)
        self.assertIn("hangar-fleet-needs-you.png", first)
        for cell in re.findall(r"\| ([^|\n]+) ", readme):
            self.assertLessEqual(len(cell.split()), 25, f"README table cell over 25 words: {cell[:60]}")

    def test_the_journey_is_told_once_and_briefly(self):
        """Seven steps on How it fits, each under 20 words with no issue numbers; Home and Flows link there."""
        fits = (ROOT / "docs" / "how-it-fits.md").read_text()
        steps = re.findall(r"^\d\. (.+)$", fits, re.M)
        self.assertEqual(len(steps), 7)
        for step in steps:
            words = re.sub(r"[`*]", "", step).split()
            self.assertLessEqual(len(words), 20, step)
            self.assertNotRegex(step, r"#\d+", step)
        self.assertNotIn("## A ticket's journey", (ROOT / "docs" / "index.md").read_text())
        self.assertNotIn("## A Jira ticket to a merged PR", (ROOT / "docs" / "architecture" / "flows.md").read_text())
