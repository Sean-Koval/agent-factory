"""Every Material / Zensical admonition type renders in Airframe's greyscale, in both themes (airframe-docs.css).

Builds the site once (offline roadmap), opens a built page in Chromium, injects one admonition and one details
block per type, and reads the computed colors of the mark, the title icon, the title background, the details chevron
and the focus ring. Everything must be a grey (or the one token the type is allowed): no Material hue may leak.

Run: python3 -m unittest discover -s tests   (needs playwright with Chromium; skipped without it)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import airframe as af  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TYPES = ("note", "abstract", "summary", "tldr", "info", "todo", "tip", "hint", "important", "success", "check", "done",
         "question", "help", "faq", "warning", "caution", "attention", "failure", "fail", "missing", "danger", "error",
         "bug", "example", "quote", "cite")
APPROVAL = {"warning", "caution", "attention"}
FAILED = {"danger", "error", "failure", "fail", "missing"}
THEMES = af.resolved(af.load_tokens())["themes"]

RGB = re.compile(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)")


def rgb(value: str) -> list[tuple[int, int, int, float]]:
    return [(int(r), int(g), int(b), float(a) if a else 1.0) for r, g, b, a in RGB.findall(value)]


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def grey(c) -> bool:
    r, g, b, a = c
    return a == 0 or max(r, g, b) - min(r, g, b) <= 12


MARKUP = "".join(
    f'<div class="admonition {t}" data-type="{t}"><p class="admonition-title">{t}</p><p>Body with <a href="#">a link</a>.</p></div>'
    f'<details class="{t}" data-type="{t}" open><summary>{t}</summary><p>Body with <a href="#">a link</a>.</p></details>'
    for t in TYPES)

READ = """() => [...document.querySelectorAll('[data-type]')].map(el => {
  const title = el.querySelector('.admonition-title, summary');
  const cs = getComputedStyle(el), ts = getComputedStyle(title);
  const before = getComputedStyle(title, '::before'), after = getComputedStyle(title, '::after');
  return {type: el.dataset.type, tag: el.tagName, shadow: cs.boxShadow, border: cs.borderLeftWidth + ' ' + cs.borderLeftColor,
          bg: cs.backgroundColor, titleBg: ts.backgroundColor, titleColor: ts.color, mark: before.backgroundColor, chevron: after.color};
})"""


def _build() -> None:
    if (SITE / "airframe" / "index.html").exists():
        return
    env = dict(os.environ, ROADMAP_ARGS="--offline")
    subprocess.run(["sh", "scripts/build_site.sh"], cwd=ROOT, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


class AdmonitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:  # pragma: no cover
            raise unittest.SkipTest("playwright is not installed")
        _build()
        cls.readings = {}
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except Exception as e:  # pragma: no cover
                raise unittest.SkipTest(f"Chromium is not available: {e}")
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto((SITE / "airframe" / "index.html").as_uri(), wait_until="load")
            page.evaluate("(m) => { const a = document.querySelector('article.md-typeset, .md-content__inner'); a.insertAdjacentHTML('beforeend', m); }", MARKUP)
            for theme, scheme in (("dark", "slate"), ("light", "default")):
                page.evaluate("(s) => document.body.setAttribute('data-md-color-scheme', s)", scheme)
                page.wait_for_timeout(100)
                cls.readings[theme] = page.evaluate(READ)
                # the focus ring: focus the link inside each block and read the box-shadow again
                focused = page.evaluate("""() => [...document.querySelectorAll('[data-type]')].map(el => {
                  el.querySelector('a').focus(); return getComputedStyle(el).boxShadow; })""")
                for reading, shadow in zip(cls.readings[theme], focused):
                    reading["focusShadow"] = shadow
            browser.close()

    def allowed(self, theme: str, t: str) -> tuple[int, int, int]:
        colors = THEMES[theme]
        if t in APPROVAL:
            return hex_rgb(colors["status-approval"])
        if t in FAILED:
            return hex_rgb(colors["status-failed"])
        return hex_rgb(colors["fg-subtle"])

    def test_every_type_is_greyscale_or_its_one_status_role(self):
        for theme, readings in self.readings.items():
            self.assertEqual(len(readings), 2 * len(TYPES), theme)
            for r in readings:
                t = r["type"]
                mark = rgb(r["mark"])[0][:3]
                self.assertEqual(mark, self.allowed(theme, t), f"{theme} {r['tag']}.{t}: title icon is {r['mark']}")
                shadow = rgb(r["shadow"])
                self.assertTrue(shadow, f"{theme} {t}: no start mark")
                self.assertEqual(shadow[0][:3], self.allowed(theme, t), f"{theme} {r['tag']}.{t}: start mark is {r['shadow']}")
                self.assertTrue(all(grey(c) for c in rgb(r["titleBg"])), f"{theme} {t}: tinted title {r['titleBg']}")
                self.assertTrue(all(grey(c) for c in rgb(r["bg"])), f"{theme} {t}: tinted block {r['bg']}")
                self.assertTrue(all(grey(c) for c in rgb(r["titleColor"])), f"{theme} {t}: title color {r['titleColor']}")
                if r["tag"] == "DETAILS":
                    self.assertTrue(all(grey(c) for c in rgb(r["chevron"])), f"{theme} {t}: chevron {r['chevron']}")
                self.assertTrue(r["border"].startswith("0px"), f"{theme} {t}: Material's colored border is back: {r['border']}")

    def test_focus_ring_is_the_focus_token_not_a_tinted_halo(self):
        for theme, readings in self.readings.items():
            focus = hex_rgb(THEMES[theme]["focus"])
            for r in readings:
                colors = rgb(r["focusShadow"])
                self.assertGreaterEqual(len(colors), 2, f"{theme} {r['type']}: {r['focusShadow']}")
                self.assertIn(focus, [c[:3] for c in colors], f"{theme} {r['type']}: focus ring {r['focusShadow']}")
                for c in colors:
                    self.assertTrue(grey(c) or c[:3] in (focus, self.allowed(theme, r["type"])), f"{theme} {r['type']}: {r['focusShadow']}")

    def test_sun_and_moon_are_in_the_sprite_for_theme_toggles(self):
        sprite = (ROOT / "theme" / "airframe-icons.svg").read_text()
        for name in ("sun", "moon"):
            self.assertIn(f'<symbol id="af-{name}"', sprite)
            self.assertTrue((ROOT / "airframe" / "icons" / f"{name}.svg").exists())
