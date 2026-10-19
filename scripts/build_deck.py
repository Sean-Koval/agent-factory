"""Build the deck: deck/src.html + theme tokens + slide drawings -> deck/index.html.

    python3 scripts/diagrams.py && python3 scripts/build_deck.py
    python3 scripts/build_deck.py --pdf      # also deck/agent-factory.pdf, one slide per page

The screen slides show the products as they are: deck/src.html references captures/<name>.png, and the build
copies docs/assets/captures/ (made by scripts/captures.py from each product's own demo) to deck/captures/, which is
not committed; scripts/build_site.sh copies them next to the published slides the same way.
"""

from __future__ import annotations

import asyncio
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECK = ROOT / "deck"
CAPTURES = ROOT / "docs" / "assets" / "captures"


def build() -> Path:
    src = (DECK / "src.html").read_text()
    tokens = (ROOT / "theme" / "airframe.css").read_text()
    src = src.replace("{{TOKENS}}", tokens)
    src = re.sub(r"\{\{SVG:([\w-]+)\}\}",
                 lambda m: (ROOT / "docs" / "assets" / "diagrams" / f"{m.group(1)}.svg").read_text(), src)
    missing = [m for m in re.findall(r'src="captures/([\w-]+\.png)"', src) if not (CAPTURES / m).exists()]
    if missing:
        raise SystemExit(f"build_deck: deck/src.html references captures that docs/assets/captures/ lacks: {missing}; "
                         "run python3 scripts/captures.py")
    shutil.rmtree(DECK / "captures", ignore_errors=True)
    shutil.copytree(CAPTURES, DECK / "captures", ignore=shutil.ignore_patterns(".*", "*.json"))
    # deck/index.html is a full document for GitHub Pages; deck/fragment.html (ignored) is the same
    # page without the document shell, for hosts that add their own.
    (DECK / "fragment.html").write_text(src)
    out = DECK / "index.html"
    # Night is the deck's theme (data-theme pins it; the tokens would otherwise follow the OS)
    out.write_text('<!doctype html>\n<html lang="en" data-theme="dark">\n<head>\n<meta charset="utf-8">\n'
                   '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                   + src.replace("</style>\n\n<main", "</style>\n</head>\n<body>\n<main", 1) + "\n</body>\n</html>\n")
    return out


async def pdf(page_file: Path) -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        tab = await browser.new_page(viewport={"width": 1280, "height": 720})
        await tab.goto(page_file.resolve().as_uri(), wait_until="networkidle")  # a URL, so captures/ resolves
        await tab.evaluate("document.fonts.ready")
        await tab.emulate_media(media="print")
        await tab.pdf(path=str(DECK / "agent-factory.pdf"), width="1280px", height="720px", print_background=True)
        await browser.close()


if __name__ == "__main__":
    out = build()
    print("wrote", out)
    if "--pdf" in sys.argv:
        asyncio.run(pdf(out))
        print("wrote", DECK / "agent-factory.pdf")
