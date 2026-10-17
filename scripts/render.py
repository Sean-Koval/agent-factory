"""Render the diagrams to PNG in both themes with the Airframe fonts.

    python3 scripts/render.py              # docs/assets/diagrams/<name>-dark.png and -light.png
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS = ROOT / "docs" / "assets" / "diagrams"
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
         "&family=DM+Mono:wght@400;500&family=Red+Hat+Text:wght@400..700&display=swap")


def page(svg: str, theme: str) -> str:
    css = (ROOT / "theme" / "airframe.css").read_text()
    return (f'<!doctype html><html data-theme="{theme}"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{FONTS}"><style>{css}'
            "html,body{margin:0;background:var(--af-canvas)} svg{display:block;width:1200px;height:auto}</style>"
            f"</head><body>{svg}</body></html>")


async def main() -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(device_scale_factor=2, viewport={"width": 1200, "height": 900})
        tab = await ctx.new_page()
        for src in sorted(DIAGRAMS.glob("*.svg")):
            for theme in ("dark", "light"):
                await tab.set_content(page(src.read_text(), theme), wait_until="networkidle")
                await tab.evaluate("document.fonts.ready")
                out = src.with_name(f"{src.stem}-{theme}.png")
                await tab.locator("svg").first.screenshot(path=str(out))
                print("wrote", out)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
