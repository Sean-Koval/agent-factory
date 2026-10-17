"""Tests for the Airframe source and build (scripts/airframe.py). Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import airframe as af  # noqa: E402

TOKENS = af.load_tokens()
THEMES = af.resolved(TOKENS)["themes"]
GROUNDS = ("canvas", "surface", "raised")


class BuildTests(unittest.TestCase):
    def test_theme_is_up_to_date_and_sources_obey_the_rules(self):
        self.assertEqual(af.problems(), [])

    def test_every_color_token_is_declared_in_both_themes(self):
        css = af.tokens_css(TOKENS)
        dark = css.split("@media")[0]
        for t in TOKENS["color"]["tokens"]:
            self.assertIn(f"--af-{t['name']}:", dark, t["name"])
        light_block = css.split('[data-theme="light"],\n[data-md-color-scheme="default"] {')[1].split("}")[0]
        for t in TOKENS["color"]["tokens"]:
            if t["value"]["light"] != t["value"]["dark"]:
                self.assertIn(f"--af-{t['name']}: {t['value']['light']};", light_block, t["name"])

    def test_theme_v1_names_still_resolve(self):
        css = af.tokens_css(TOKENS)
        for old in ("st-appr", "st-fail", "p-hangar", "p-workspace", "f-mono", "r-card", "term-bg", "dot"):
            self.assertRegex(css, rf"--af-{old}: var\(--af-[a-z0-9-]+\);")

    def test_check_catches_a_color_literal(self):
        self.assertEqual(af.color_literals(".x{color:#fff}/* #000 in a comment is fine */"), ["#fff"])
        self.assertEqual(af.color_literals(".x{background:rgba(0,0,0,.5)}"), ["rgba("])
        self.assertEqual(af.color_literals(".x{color:var(--af-fg)}"), [])

    def test_gallery_and_pages_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            n = af.gallery(Path(tmp) / "gallery")
            self.assertGreaterEqual(n, 20)
            index = (Path(tmp) / "gallery" / "index.html").read_text()
            self.assertIn('href="Status.html"', index)
            self.assertTrue((Path(tmp) / "gallery" / "airframe-components.css").exists())
            written = af.pages(Path(tmp) / "pages")
            self.assertIn("--af-status-approval", (Path(tmp) / "pages" / "airframe-colors.md").read_text())
            self.assertEqual(len(written), 5)


class ContrastTests(unittest.TestCase):
    """The accessibility floor every release keeps (WCAG 2.x)."""

    def assertContrast(self, fg: str, minimum: float, grounds=GROUNDS):
        for theme, values in THEMES.items():
            for bg in grounds:
                ratio = af.contrast(values[fg], values[bg])
                self.assertGreaterEqual(ratio, minimum, f"{fg} on {bg} in {theme}: {ratio:.2f}")

    def test_text(self):
        for fg in ("fg", "fg-muted", "fg-subtle", "brand-text", "status-approval", "status-failed",
                   "status-running", "status-queued"):
            self.assertContrast(fg, 4.5)

    def test_lines_focus_and_marks(self):
        for fg in ("line-strong", "focus", "status-off", "product-hangar", "product-flightdeck",
                   "product-tower", "product-aidlc", "product-spaceport"):
            self.assertContrast(fg, 3.0)

    def test_text_on_fills(self):
        for theme, v in THEMES.items():
            for fg, bg in (("on-brand", "brand"), ("on-status-denied", "status-denied"),
                           ("on-lamp", "lamp-caution"), ("on-lamp", "lamp-warning"),
                           ("terminal-fg", "terminal-bg"), ("terminal-dim", "terminal-bg"),
                           ("code-comment", "terminal-bg")):
                self.assertGreaterEqual(af.contrast(v[fg], v[bg]), 4.5, f"{fg} on {bg} in {theme}")

    def test_brand_is_never_a_status(self):
        for theme, v in THEMES.items():
            statuses = {v[k].upper() for k in v if k.startswith("status-")}
            self.assertNotIn(v["brand"].upper(), statuses, theme)


class SourceTests(unittest.TestCase):
    def test_components_document_themselves(self):
        for comp in sorted(p for p in (af.SRC / "components").iterdir() if p.is_dir() and p.name != "Cover"):
            first = (comp / "preview.html").read_text().split("\n", 1)[0]
            self.assertRegex(first, r'^<!-- @dsCard group="[A-Za-z]+" height=\d+', comp.name)
            self.assertTrue(af.summary(comp / "README.md"), f"{comp.name}: README needs a one-line summary")

    def test_icons_are_stroke_only_on_the_20px_grid(self):
        for svg in sorted((af.SRC / "icons").glob("*.svg")):
            if svg.name == "airframe-icons.svg":
                continue
            text = svg.read_text()
            self.assertIn('viewBox="0 0 20 20"', text, svg.name)
            self.assertIsNone(re.search(r'stroke="#|fill="#', text), f"{svg.name}: color it with currentColor")


if __name__ == "__main__":
    unittest.main()
