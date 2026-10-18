"""Tests for the brand surfaces (scripts/banners.py). Run: python3 -m unittest discover -s tests

Needs fonttools and uharfbuzz, like the generator; without them the suite is skipped, not failed."""

from __future__ import annotations

import json
import re
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import banners  # noqa: E402

try:
    import uharfbuzz  # noqa: F401
    import fontTools  # noqa: F401
    HAVE_FONT_TOOLS = True
except ImportError:  # pragma: no cover
    HAVE_FONT_TOOLS = False

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
MARKS = banners.load_marks()
THEMES = banners.load_themes()


@unittest.skipUnless(HAVE_FONT_TOOLS, "fonttools and uharfbuzz are needed to shape the banners")
class BannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = banners.outputs()

    def test_committed_brand_files_are_up_to_date(self):
        self.assertEqual(banners.problems(), [])

    def test_every_product_gets_the_full_set(self):
        for product in banners.PRODUCTS:
            for name in ("banner-dark.svg", "banner-light.svg", "social-dark.svg", "social-light.svg", "favicon.svg", "mark.svg"):
                self.assertIn(banners.OUT / product / name, self.outputs, f"{product}/{name}")

    def test_text_is_outlined_and_no_font_is_referenced(self):
        """GitHub shows README images as <img> through its proxy: no web fonts load, so no <text> may remain."""
        for path, svg in self.outputs.items():
            if path.name.startswith(("banner", "social")):
                self.assertNotIn("<text", svg, path.name)
                self.assertNotIn("font-family", svg, path.name)
                self.assertIn("<use href=", svg, path.name)

    def test_every_color_is_that_themes_token_value(self):
        for path, svg in self.outputs.items():
            if path.name.startswith(("banner", "social")):
                theme = "dark" if "dark" in path.name else "light"
                allowed = {v.upper() for v in THEMES[theme].values() if isinstance(v, str) and HEX.fullmatch(v)}
                for color in HEX.findall(svg):
                    self.assertIn(color.upper(), allowed, f"{path.relative_to(banners.ROOT)}: {color} is not a {theme} token value")

    def test_product_hue_appears_only_in_the_mark_and_the_suite_marker(self):
        """The glyph (color and stroke) and the 2px suite marker, nothing else; for the family mark, whose hue is
        brand-text, the third use is the eyebrow hairline (brand-line has the same value)."""
        for product, p in banners.PRODUCTS.items():
            hue = MARKS[p["mark"]]["hue"]
            for theme in ("dark", "light"):
                svg = self.outputs[banners.OUT / product / f"banner-{theme}.svg"]
                value = THEMES[theme][hue]
                uses = len(re.findall(re.escape(value), svg, re.I))
                self.assertLessEqual(uses, 3, f"{product} {theme}: hue used {uses} times")

    def test_banner_and_social_sizes(self):
        for path, svg in self.outputs.items():
            if path.name.startswith("banner"):
                self.assertIn('width="960" height="320"', svg)
            if path.name.startswith("social"):
                self.assertIn('width="1280" height="640"', svg)

    def test_social_png_is_what_github_accepts(self):
        """1280x640 PNG under 1 MB (docs.github.com, customizing your repository's social media preview)."""
        for product in banners.PRODUCTS:
            png = banners.OUT / product / "social.png"
            if not png.exists():
                continue
            data = png.read_bytes()
            self.assertLess(len(data), 1_000_000, product)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n", product)
            w, h = struct.unpack(">II", data[16:24])
            self.assertEqual((w, h), (1280, 640), product)

    def test_favicon_and_mark_follow_the_color_scheme(self):
        for product, p in banners.PRODUCTS.items():
            hue = MARKS[p["mark"]]["hue"]
            for name in ("favicon.svg", "mark.svg"):
                svg = self.outputs[banners.OUT / product / name]
                self.assertIn("@media (prefers-color-scheme: light)", svg, f"{product}/{name}")
                self.assertIn(THEMES["dark"][hue], svg)
                self.assertIn(THEMES["light"][hue], svg)
                self.assertIn('aria-label=', svg)

    def test_lines_fit_two_rows(self):
        faces = banners.load_faces()
        for product in banners.PRODUCTS:
            for theme in ("dark", "light"):
                banners.banner(product, theme, banners.BANNER, faces, MARKS, THEMES)  # raises when a line is too long


class MarksTests(unittest.TestCase):
    def test_marks_json_matches_the_product_marks_readme(self):
        """The component README documents the glyphs; marks.json is what the generators read. They must agree."""
        readme = (banners.ROOT / "airframe" / "components" / "ProductMarks" / "README.md").read_text()
        for key, m in MARKS.items():
            self.assertIn(m["glyph"], readme, f"{key}: glyph in marks.json is not the one in the ProductMarks README")
            self.assertIn(m["hue"], readme, key)

    def test_marks_are_stroke_only_on_the_24px_grid(self):
        for key, m in MARKS.items():
            self.assertIsNone(re.search(r'stroke="#|fill="#', m["glyph"]), f"{key}: color it with currentColor")
            self.assertIn(m["hue"], THEMES["dark"], key)
            self.assertIn(m["hue"], THEMES["light"], key)

    def test_every_banner_product_has_a_mark(self):
        for product, p in banners.PRODUCTS.items():
            self.assertIn(p["mark"], MARKS, product)

    def test_fonts_are_vendored_with_their_licenses(self):
        for key, name in banners.FONT_FILES.items():
            self.assertTrue((banners.FONTS / name).exists(), name)
            self.assertTrue((banners.FONTS / f"OFL-{name.split('-')[0]}.txt").exists(), name)


if __name__ == "__main__":
    unittest.main()
