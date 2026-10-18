#!/usr/bin/env python3
"""Brand surfaces generated from Airframe: README banners, social previews, marks and favicons.

    python3 scripts/banners.py                 # writes brand/<product>/*.svg (text as outlines) and docs/assets/brand/
    python3 scripts/banners.py --png           # also the PNGs (Playwright + Chromium)
    python3 scripts/banners.py check           # CI: the committed SVGs match what the sources produce
    python3 scripts/banners.py fonts           # re-derive airframe/fonts/ from google/fonts (network)

Per product, brand/<product>/ holds:

    banner-dark.svg, banner-light.svg     960x320 README banner, Night and Day (use both in a <picture>)
    banner-dark.png, banner-light.png     the same at 2x, for places that take no SVG (Slack, decks)
    social.png                            1280x640 GitHub social preview, Night (under 1 MB)
    favicon.svg                           32x32 mark on canvas; follows prefers-color-scheme
    mark.svg                              44x44 mark tile (docs header, app header)

Sources: theme/airframe-tokens.json (built from airframe/tokens.json), airframe/icons/marks.json (the product
glyphs) and the subset fonts in airframe/fonts/. Every color in an output is a token's value for that theme;
the product hue appears only in the mark and the 2px suite marker. Text is converted to outlines because
GitHub serves README images through its proxy as <img>, which loads no web fonts and no external files.

Needs fonttools and uharfbuzz (pip install fonttools uharfbuzz); --png also needs playwright.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "theme" / "airframe-tokens.json"
MARKS = ROOT / "airframe" / "icons" / "marks.json"
FONTS = ROOT / "airframe" / "fonts"
OUT = ROOT / "brand"
DOCS_BRAND = ROOT / "docs" / "assets" / "brand"

BANNER = (960, 320)
SOCIAL = (1280, 640)

# Copy per product: the eyebrow names the suite and the plane, the line says what the product does.
# Names and casing follow airframe/guide/brand.md; the lines are each product's own lede, shortened.
PRODUCTS = {
    "agent-factory": {
        "mark": "airframe", "name": "Agent factory", "plane": "Suite home",
        "eyebrow": "Suite home · Docs, deck, diagrams, Airframe",
        "line": "Define, run, judge and govern cloud coding agents for a team.",
    },
    "airframe": {
        "mark": "airframe", "name": "Airframe", "plane": "Design system",
        "line": "Agent infrastructure, quiet until a human is needed.",
    },
    "hangar": {
        "mark": "hangar", "name": "hangar", "plane": "Run plane",
        "line": "Hand a ticket to a coding agent in an isolated cloud sandbox, and get back a verified draft pull request.",
    },
    "flightdeck": {
        "mark": "flightdeck", "name": "flightdeck", "plane": "Judge plane",
        "line": "Did that harness change help? Paired statistics and behavior specs over the runs hangar records, and a verdict on the PR.",
    },
    "tower": {
        "mark": "tower", "name": "Tower", "plane": "Govern plane",
        "line": "One decision point for risky agent actions: rules, human approvals and signed receipts.",
    },
    "ai-dlc": {
        "mark": "aidlc", "name": "ai-dlc", "plane": "Define plane",
        "line": "One pinned machine profile, one workflow for people and agents, and a finish that needs merged evidence.",
    },
    "spaceport": {
        "mark": "spaceport", "name": "Spaceport", "plane": "Capability plane",
        "line": "Reviewed data products that people and agents discover and query through one governed API.",
    },
}

# The suite strip along the bottom of a banner: the four planes and the capability, in the docs' order.
SUITE = (("Define", "ai-dlc"), ("Run", "hangar"), ("Judge", "flightdeck"), ("Govern", "tower"), ("Capability", "spaceport"))

FONT_FILES = {"display": "Archivo-ExpandedBold.ttf", "sans": "RedHatText-Regular.ttf", "mono": "DMMono-Medium.ttf"}

# Where airframe/fonts/ comes from: google/fonts at a pinned commit, instanced and subset by `fonts`.
GOOGLE_FONTS = "47d54ca1ebb14fd864695f1d39dc734f39017c33"
FONT_SOURCES = {
    "display": ("ofl/archivo/Archivo[wdth,wght].ttf", {"wdth": 125, "wght": 700}),
    "sans": ("ofl/redhattext/RedHatText[wght].ttf", {"wght": 400}),
    "mono": ("ofl/dmmono/DMMono-Medium.ttf", None),
}
FONT_LICENSES = {"display": "ofl/archivo/OFL.txt", "sans": "ofl/redhattext/OFL.txt", "mono": "ofl/dmmono/OFL.txt"}
SUBSET = "U+0020-007E,U+00A0,U+00B7,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2026"


def load_marks() -> dict:
    return {k: v for k, v in json.loads(MARKS.read_text()).items() if not k.startswith("_")}


def load_themes() -> dict:
    return json.loads(TOKENS.read_text())["themes"]


def num(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------- type as outlines

class Face:
    """One font: HarfBuzz shapes the text (kerning included), fontTools gives each glyph's outline."""

    def __init__(self, key: str, path: Path):
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont

        self.key = key
        self.font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
        self.upem = self.font.face.upem
        self.tt = TTFont(str(path))
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        os2 = self.tt["OS/2"]
        self.cap = os2.sCapHeight / self.upem
        self.xh = os2.sxHeight / self.upem

    def shape(self, text: str, size: float, tracking: float = 0.0) -> tuple[list[tuple[int, float, float]], float]:
        import uharfbuzz as hb

        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        s = size / self.upem
        x, out = 0.0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((info.codepoint, x + pos.x_offset * s, -pos.y_offset * s))
            x += pos.x_advance * s + tracking
        return out, x - (tracking if out else 0)

    def width(self, text: str, size: float, tracking: float = 0.0) -> float:
        return self.shape(text, size, tracking)[1]

    def outline(self, gid: int) -> str:
        from fontTools.pens.svgPathPen import SVGPathPen

        pen = SVGPathPen(self.glyphs, ntos=num)
        self.glyphs[self.order[gid]].draw(pen)
        return pen.getCommands()


class Canvas:
    """Collects SVG elements and the glyph <defs> they use."""

    def __init__(self, faces: dict[str, Face]):
        self.faces = faces
        self.defs: dict[str, str] = {}
        self.body: list[str] = []

    def add(self, *elements: str) -> None:
        self.body.extend(elements)

    def text(self, face: str, s: str, x: float, y: float, size: float, fill: str, tracking_em: float = 0.0,
             upper: bool = False, anchor: str = "start") -> float:
        """Set s at baseline (x, y) as outlines; returns the advance width."""
        f = self.faces[face]
        if upper:
            s = s.upper()
        glyphs, width = f.shape(s, size, tracking_em * size)
        if anchor == "end":
            x -= width
        elif anchor == "middle":
            x -= width / 2
        scale = f"{size / f.upem:.5f}".rstrip("0")
        uses = []
        for gid, gx, gy in glyphs:
            gid_id = f"{f.key}{gid}"
            if gid_id not in self.defs:
                self.defs[gid_id] = f.outline(gid)
            if not self.defs[gid_id]:
                continue  # space
            uses.append(f'<use href="#{gid_id}" transform="translate({num(x + gx)} {num(y + gy)}) scale({scale} -{scale})"/>')
        self.add(f'<g fill="{fill}">{"".join(uses)}</g>')
        return width

    def wrap(self, face: str, s: str, max_width: float, size: float, tracking_em: float = 0.0) -> list[str]:
        f = self.faces[face]
        lines, cur = [], ""
        for word in s.split():
            trial = f"{cur} {word}".strip()
            if cur and f.width(trial, size, tracking_em * size) > max_width:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines

    def svg(self, w: int, h: int, title: str, desc: str) -> str:
        defs = "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.defs.items() if d)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
                f"<title id=\"t\">{esc(title)}</title><desc id=\"d\">{esc(desc)}</desc>"
                f"<defs>{defs}</defs>{''.join(self.body)}</svg>\n")


# ---------------------------------------------------------------- marks

def mark_svg(glyph: str, hue: str, line: str, size: float, x: float, y: float, stroke: float = 1.6) -> str:
    """The ProductMarks tile: transparent, 1px line-strong border, radius-control, glyph in the hue.
    Glyph box is 0.636 of the tile, as in core.css (19/30, 28/44)."""
    g = size * 0.636
    o = (size - g) / 2
    s = f"{g / 24:.4f}".rstrip("0")
    return (f'<rect x="{num(x + 0.5)}" y="{num(y + 0.5)}" width="{num(size - 1)}" height="{num(size - 1)}" rx="2" '
            f'fill="none" stroke="{line}"/>'
            f'<g transform="translate({num(x + o)} {num(y + o)}) scale({s})" fill="none" color="{hue}" stroke="{hue}" '
            f'stroke-width="{num(stroke)}" stroke-linecap="square" stroke-linejoin="miter">{glyph}</g>')


def themed_mark(product: str, marks: dict, themes: dict, size: int, favicon: bool) -> str:
    """A stand-alone mark that follows the viewer's color scheme (Night values first, Day under a media query).
    The favicon sits on canvas so it reads on any tab strip; the header mark is the transparent tile."""
    m = marks[product]
    dark, light = themes["dark"], themes["light"]
    stroke = 2.2 if favicon else 1.6
    g = size * (0.75 if favicon else 0.636)
    o = (size - g) / 2
    hue_d, hue_l = dark[m["hue"]], light[m["hue"]]
    css = (".bg{fill:%s}.tile{fill:none;stroke:%s}.glyph{fill:none;color:%s;stroke:%s;stroke-width:%s;stroke-linecap:square;stroke-linejoin:miter}"
           "@media (prefers-color-scheme: light){.bg{fill:%s}.tile{stroke:%s}.glyph{color:%s;stroke:%s}}" % (
               dark["canvas"], dark["line-strong"], hue_d, hue_d, num(stroke),
               light["canvas"], light["line-strong"], hue_l, hue_l))
    bg = f'<rect class="bg" width="{size}" height="{size}" rx="2"/>' if favicon else ""
    inset = 1.5 if favicon else 0.5
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'role="img" aria-label="{esc(m["name"])}"><style>{css}</style>{bg}'
            f'<rect class="tile" x="{num(inset)}" y="{num(inset)}" width="{num(size - 2 * inset)}" height="{num(size - 2 * inset)}" rx="2"/>'
            f'<g class="glyph" transform="translate({num(o)} {num(o)}) scale({g / 24:.4f})">{m["glyph"]}</g></svg>\n')


# ---------------------------------------------------------------- the banner

def dots(cv: Canvas, pid: str, color: str, x: float, y: float, w: float, h: float) -> None:
    cv.add(f'<pattern id="{pid}" x="{num(x)}" y="{num(y)}" width="8" height="8" patternUnits="userSpaceOnUse">'
           f'<circle cx="4" cy="4" r="1.1" fill="{color}"/></pattern>'
           f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="url(#{pid})"/>')


def banner(product: str, theme: str, size: tuple[int, int], faces: dict[str, Face], marks: dict, themes: dict,
           strip: bool = True) -> str:
    """The lockup banner: eyebrow, mark + name in the display face, the product's line, and the suite strip
    with a 2px marker in the product hue under its own plane. Hue appears nowhere else."""
    p, v = PRODUCTS[product], themes[theme]
    m = marks[p["mark"]]
    W, H = size
    s = W / BANNER[0]                       # the composition is designed at 960x320 and scales with the width
    oy = (H - BANNER[1] * s) / 2            # and centers vertically when the canvas is taller (social preview)
    cv = Canvas(faces)
    cv.add(f'<rect width="{W}" height="{H}" fill="{v["canvas"]}"/>')
    L, STRIP, DOTS_X = 64, 268, BANNER[0] - 320
    # dot field: the hero texture, top right, from the top edge down to just above the suite rule
    dots(cv, "dots", v["dot-field"], DOTS_X * s, 0, 320 * s, oy + (STRIP - 12) * s)
    cv.add(f'<g transform="translate(0 {num(oy)}) scale({num(s)})">')
    # eyebrow: brand hairline and the suite · plane label in mono capitals
    cv.add(f'<rect x="{L}" y="55.5" width="18" height="1" fill="{v["brand-line"]}"/>')
    cv.text("mono", p.get("eyebrow", f"Agent factory · {p['plane']}"), L + 28, 60, 12, v["fg-subtle"], tracking_em=0.08, upper=True)
    # lockup: the mark at 72px beside the name (84px, smaller only when a long name would reach the dot field)
    mark_size, base, name_x = 72, 166, L + 72 + 22
    name_size = 84
    name_w = faces["display"].width(p["name"], name_size, -0.01 * name_size)
    if name_x + name_w > DOTS_X - 12:
        name_size = 84 * (DOTS_X - 12 - name_x) / name_w
    cap = faces["display"].cap * name_size
    cv.add(mark_svg(m["glyph"], v[m["hue"]], v["line-strong"], mark_size, L, base - cap / 2 - mark_size / 2))
    cv.text("display", p["name"], name_x, base, name_size, v["fg"], tracking_em=-0.01)
    # the line: body face, fg-muted, two lines at most, clear of the dot field
    lines = cv.wrap("sans", p["line"], DOTS_X - 24 - L, 19)
    if len(lines) > 2:
        raise ValueError(f"{product}: the line needs {len(lines)} rows at 19px; shorten it to fit two")
    y = 208
    for line in lines:
        cv.text("sans", line, L, y, 19, v["fg-muted"])
        y += 27
    if strip:
        # suite strip: rule, five columns, the current plane in fg with the nav marker in the product hue
        cv.add(f'<rect x="{L}" y="{STRIP}" width="{BANNER[0] - 2 * L}" height="1" fill="{v["rule"]}"/>')
        col = (BANNER[0] - 2 * L) / len(SUITE)
        for i, (plane, prod) in enumerate(SUITE):
            x = L + i * col
            here = prod == product
            cv.text("mono", plane, x, STRIP + 19, 9.5, v["fg-subtle"] if here else v["fg-dim"], tracking_em=0.09, upper=True)
            w = cv.text("display", PRODUCTS[prod]["name"], x, STRIP + 34, 12, v["fg"] if here else v["fg-subtle"])
            if here:
                cv.add(f'<rect x="{num(x)}" y="{STRIP - 1}" width="{num(w)}" height="2" fill="{v[m["hue"]]}"/>')
    cv.add("</g>")
    title = f"{p['name']}: {p['line']}"
    desc = f"{p['name']} banner in Airframe's {'Night' if theme == 'dark' else 'Day'} theme: the {p['name']} mark, the name, and its place in the agent factory suite ({p['plane'].lower()})."
    return cv.svg(W, H, title, desc)


# ---------------------------------------------------------------- outputs

def load_faces() -> dict[str, Face]:
    return {k: Face(k[0], FONTS / f) for k, f in FONT_FILES.items()}


def outputs(faces: dict[str, Face] | None = None) -> dict[Path, str]:
    """Every SVG, keyed by its path under brand/ (PNGs come from these; see render)."""
    faces = faces or load_faces()
    marks, themes = load_marks(), load_themes()
    out: dict[Path, str] = {}
    for product, p in PRODUCTS.items():
        d = OUT / product
        for theme in ("dark", "light"):
            out[d / f"banner-{theme}.svg"] = banner(product, theme, BANNER, faces, marks, themes)
            out[d / f"social-{theme}.svg"] = banner(product, theme, SOCIAL, faces, marks, themes)
        out[d / "favicon.svg"] = themed_mark(p["mark"], marks, themes, 32, favicon=True)
        out[d / "mark.svg"] = themed_mark(p["mark"], marks, themes, 44, favicon=False)
    # the suite docs site's own tab icon and header mark (mkdocs.yml theme.favicon / theme.logo)
    for name in ("favicon.svg", "mark.svg"):
        out[DOCS_BRAND / name] = out[OUT / "agent-factory" / name]
    return out


def build() -> list[Path]:
    written = []
    for path, text in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text() != text:
            path.write_text(text)
            written.append(path)
    return written


def problems() -> list[str]:
    found = []
    for path, text in outputs().items():
        if not path.exists() or path.read_text() != text:
            found.append(f"{path.relative_to(ROOT)} is out of date; run python3 scripts/banners.py")
    return found


async def render() -> None:
    """PNGs from the SVGs: banners at 2x, the social preview at 1x (GitHub wants PNG under 1 MB)."""
    from playwright.async_api import async_playwright

    jobs = []
    for product in PRODUCTS:
        d = OUT / product
        for theme in ("dark", "light"):
            jobs.append((d / f"banner-{theme}.svg", d / f"banner-{theme}.png", BANNER, 2))
        jobs.append((d / "social-dark.svg", d / "social.png", SOCIAL, 1))
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for src, dst, (w, h), scale in jobs:
            ctx = await browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale)
            tab = await ctx.new_page()
            await tab.set_content(f'<!doctype html><html><body style="margin:0">{src.read_text()}</body></html>')
            await tab.locator("svg").first.screenshot(path=str(dst), omit_background=False)
            await ctx.close()
            print("wrote", dst.relative_to(ROOT), dst.stat().st_size, "bytes")
        await browser.close()


def derive_fonts() -> None:
    """Fetch the three families from google/fonts at the pinned commit, instance the variable ones
    (Archivo at wdth 125 / wght 700 is Archivo Expanded Bold; Red Hat Text at wght 400) and subset to Latin.
    The results and their OFL texts are committed; GitHub-served images never load fonts, so these are
    build inputs only."""
    import urllib.parse
    import urllib.request

    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    base = f"https://raw.githubusercontent.com/google/fonts/{GOOGLE_FONTS}/"
    FONTS.mkdir(exist_ok=True)
    for key, (src, axes) in FONT_SOURCES.items():
        with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
            urllib.request.urlretrieve(base + urllib.parse.quote(src), tmp.name)
            font = TTFont(tmp.name)
        if axes:
            font = instancer.instantiateVariableFont(font, axes, inplace=False, updateFontNames=True)
        opts = subset.Options()
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        opts.desubroutinize = True
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=subset.parse_unicodes(SUBSET))
        sub.subset(font)
        font.save(FONTS / FONT_FILES[key])
        lic = FONTS / f"OFL-{FONT_FILES[key].split('-')[0]}.txt"
        urllib.request.urlretrieve(base + FONT_LICENSES[key], lic)
        print("wrote", FONTS / FONT_FILES[key], "and", lic.name)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="build", choices=["build", "check", "fonts"])
    ap.add_argument("--png", action="store_true", help="also render the PNGs (needs Playwright)")
    a = ap.parse_args(argv)
    if a.command == "fonts":
        derive_fonts()
        return 0
    if a.command == "check":
        found = problems()
        for f in found:
            print(f, file=sys.stderr)
        print("brand/ is up to date" if not found else f"{len(found)} problem(s)")
        return 1 if found else 0
    for path in build():
        print("wrote", path.relative_to(ROOT))
    if a.png:
        import asyncio

        asyncio.run(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
