"""Build the self-contained deck: deck/src.html + theme tokens + slide drawings -> deck/index.html.

    python3 scripts/diagrams.py && python3 scripts/build_deck.py
    python3 scripts/build_deck.py --pdf      # also deck/agent-factory.pdf, one slide per page
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECK = ROOT / "deck"


def build() -> Path:
    src = (DECK / "src.html").read_text()
    tokens = (ROOT / "theme" / "airframe.css").read_text()
    src = src.replace("{{TOKENS}}", tokens)
    src = re.sub(r"\{\{SVG:([\w-]+)\}\}",
                 lambda m: (ROOT / "docs" / "assets" / "diagrams" / f"{m.group(1)}.svg").read_text(), src)
    # deck/index.html is a full document for GitHub Pages; deck/fragment.html (ignored) is the same
    # page without the document shell, for hosts that add their own.
    (DECK / "fragment.html").write_text(src)
    out = DECK / "index.html"
    out.write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                   '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                   + src.replace("</style>\n\n<main", "</style>\n</head>\n<body>\n<main", 1) + "\n</body>\n</html>\n")
    return out


async def pdf(page_file: Path) -> None:
    from playwright.async_api import async_playwright

    html = page_file.read_text()
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        tab = await browser.new_page(viewport={"width": 1280, "height": 720})
        await tab.set_content(html, wait_until="networkidle")
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
