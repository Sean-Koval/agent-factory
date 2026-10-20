"""The built docs site: every embedded frame points at a page that exists in site/.

Builds the site once (offline roadmap) and checks the Deck page's iframe, whose src Zensical
rewrites relative to the page: a src that resolves outside site/ is the 404 a visitor saw.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import os
import posixpath
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
IFRAME = re.compile(r"<iframe\b[^>]*\bsrc=\"([^\"]+)\"")


def _build() -> None:
    env = dict(os.environ, ROADMAP_ARGS="--offline")
    subprocess.run(["sh", "scripts/build_site.sh"], cwd=ROOT, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _target(page: Path, src: str) -> Path:
    """The file a frame on `page` (site/.../index.html) loads for `src`, as the server would resolve it."""
    if src.startswith(("http:", "https:", "//")):
        raise AssertionError(f"{page.relative_to(SITE)} embeds a remote frame {src!r}")
    base = "/" + page.relative_to(SITE).parent.as_posix().strip(".") + "/"
    path = posixpath.normpath(posixpath.join(base, src.split("?")[0].split("#")[0]))
    if path.startswith("/.."):
        raise AssertionError(f"{page.relative_to(SITE)} frame src {src!r} leaves the site")
    target = SITE / path.lstrip("/")
    return target / "index.html" if src.endswith("/") or target.is_dir() else target


@unittest.skipUnless(shutil.which(os.environ.get("ZENSICAL", "zensical")), "zensical is not installed")
class BuiltSiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _build()

    def test_deck_page_frames_the_slides(self) -> None:
        page = SITE / "deck" / "index.html"
        srcs = IFRAME.findall(page.read_text())
        self.assertEqual(len(srcs), 1, "the Deck page embeds the slides once")
        target = _target(page, srcs[0])
        self.assertTrue(target.is_file(), f"iframe src {srcs[0]!r} resolves to {target}, which does not exist")
        self.assertIn('class="slide', target.read_text(), f"{target} is not the slides")

    def test_every_frame_target_exists(self) -> None:
        missing = []
        for page in sorted(SITE.rglob("index.html")):
            for src in IFRAME.findall(page.read_text()):
                if not _target(page, src).is_file():
                    missing.append(f"{page.relative_to(SITE)}: {src}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
