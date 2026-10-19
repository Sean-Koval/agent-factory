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
NAMES = {f"{base}-{crop}": (base, crop) for base, crops in captures.CROPS.items() for crop in crops}


def surfaces(name: str) -> tuple[str, ...]:
    """Where the crop file <name>.png is cut to be shown; () for a file that is not a named crop."""
    base, crop = NAMES.get(name, (None, None))
    return captures.CROPS[base][crop][2] if base else ()


class CropTests(unittest.TestCase):
    def test_every_named_crop_is_cut_from_its_capture_and_listed(self):
        """A crop is derived, never drawn: it exists, has the box's size and is in captures.json."""
        from PIL import Image

        manifest = json.loads((OUT / "captures.json").read_text())
        for name, crops in captures.CROPS.items():
            self.assertTrue((OUT / f"{name}.png").exists(), f"{name}: full capture missing")
            for crop, ((x, y, w, h), shows, where) in crops.items():
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
            for name in shown:
                self.assertIn(name, NAMES, f"{page.name} shows {name}, which is not a named crop")

    def test_every_crop_is_legible_where_it_is_shown(self):
        """A crop is cut no wider (or taller) than the surface shows it divided by LEGIBLE, so the product's 13 px labels
        render at 11 px or more on the home hero, a tool page and a deck slide."""
        for name, crops in captures.CROPS.items():
            for crop, ((x, y, w, h), _, where) in crops.items():
                self.assertTrue(where, f"{name}-{crop}: say where it is shown")
                for surface in where:
                    sw, sh = captures.SHOWN[surface]
                    scale = min(sw / w, sh / h, 1)
                    self.assertGreaterEqual(scale, captures.LEGIBLE, f"{name}-{crop} on the {surface} renders at {scale:.2f}: 13 px labels at {13 * scale:.1f} px")

    def test_the_hero_shows_a_crop_cut_for_it(self):
        home = (ROOT / "docs" / "index.md").read_text()
        hero = home.split('class="af-hero__visual"')[1].split("</figure>")[0]
        name = re.search(r'src="assets/captures/([\w-]+)\.png"', hero).group(1)
        self.assertIn("hero", surfaces(name), f"{name} is not cut for the hero")

    def test_tool_pages_show_crops_cut_for_a_page(self):
        for page in sorted((ROOT / "docs" / "tools").glob("*.md")):
            for name in re.findall(r'src="\.\./assets/captures/([\w-]+)\.png"', page.read_text()):
                self.assertIn("page", surfaces(name), f"{page.name} shows {name}, which is not cut for a tool page")

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
