#!/usr/bin/env python3
"""Airframe build: airframe/ is the source, theme/ is what the sites and the tool repos load.

    python3 scripts/airframe.py build          # regenerate the theme/ files below from airframe/
    python3 scripts/airframe.py check          # CI: theme/ is up to date and the sources obey the rules
    python3 scripts/airframe.py gallery DIR    # component previews in Night and Day (the docs site's gallery)
    python3 scripts/airframe.py pages DIR      # reference tables (tokens, components, icons) as Markdown snippets
    python3 scripts/airframe.py registry DIR   # the shadcn-compatible registry as static JSON (the docs site's /r/)

Generated (never edit by hand):

    theme/airframe.css             every token as --af-<name>, both themes, plus the theme-v1 names as aliases
    theme/airframe-components.css  the af- component classes: fonts, type styles, base, core, agents, patterns, viz
    theme/airframe-icons.svg       the icon sprite (<use href="airframe-icons.svg#af-agent">)
    theme/airframe.js              the optional helpers (markup builders, toast, confirm, drawer), copied from airframe/js/
    theme/airframe-tokens.json     tokens resolved per theme, for scripts (diagrams, decks, tests)
    theme/airframe-tailwind.css    a Tailwind CSS v4 @theme that maps every utility onto the --af- tokens
    theme/airframe.tokens.json     the tokens in the W3C Design Tokens (DTCG 2025.10) format, Night
    theme/airframe-day.tokens.json the same for Day (one complete file per theme; tools merge or pick)
    theme/airframe-docs.css        the docs-site mapping (Material for MkDocs / Zensical), from airframe/docs-site/
    theme/airframe-suite.html      the suite strip partial above every docs header, from airframe/docs-site/

The registry: registry.json at the repo root lists the items (a GitHub source registry: `npx shadcn@latest
add Sean-Koval/agent-factory/<item>#theme-vN`); `registry` inlines each item's files into DIR/<item>.json
so the same items install from the docs site (`npx shadcn@latest add <site>/r/<item>.json`).

Hand-written in theme/: suite.css (this site only) and CHANGELOG.md.
No dependencies beyond the Python standard library.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "airframe"
THEME = ROOT / "theme"
TOKENS = SRC / "tokens.json"
STYLES = ("base.css", "core.css", "agents.css", "patterns.css", "viz.css")
HELPERS = SRC / "js" / "airframe.js"
DOCS_SITE = SRC / "docs-site"
THUMBS = ROOT / "docs" / "assets" / "airframe"  # one Night thumbnail per component, from scripts/captures.py airframe  # the docs mapping and the suite strip, published as theme/airframe-docs.css and -suite.html
FONTS_URL = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
             "&family=DM+Mono:wght@400;500&family=Red+Hat+Text:ital,wght@0,400..700;1,400..700&display=swap")
PREFIX = "--af-"
THEMED = ("color", "shadow")
PLAIN = ("font", "spacing", "radius", "layout", "icon")

# theme-v1 names (the first tagged release) -> the token that replaced them. Kept as aliases so
# anything written against theme-v1 keeps working; new code uses the names on the right.
ALIASES = {
    "st-run": "status-running", "st-queue": "status-queued", "st-appr": "status-approval",
    "st-fail": "status-failed", "st-deny": "status-denied", "st-off": "status-off",
    "p-hangar": "product-hangar", "p-flightdeck": "product-flightdeck", "p-workspace": "product-tower",
    "p-tower": "product-tower", "product-workspace": "product-tower", "p-aidlc": "product-aidlc",
    "p-spaceport": "product-spaceport",
    "term-bg": "terminal-bg", "term-fg": "terminal-fg",
    "code-k": "code-keyword", "code-f": "code-function", "code-s": "code-string",
    "code-n": "code-number", "code-c": "code-comment",
    "dot": "dot-field",
    "f-display": "font-display", "f-sans": "font-sans", "f-mono": "font-mono",
    "r-ctl": "radius-control", "r-card": "radius-card", "r-chip": "radius-control",
    "pad": "space-16", "gap": "space-12",
}

# Theme scopes. Night is the default; Day follows the OS until a page pins a theme. The docs sites
# switch with data-md-color-scheme on <body>. Any element can open a nested scope with data-theme.
DARK_SCOPE = ':root,\n[data-theme="dark"],\n[data-md-color-scheme="slate"]'
LIGHT_SCOPE = '[data-theme="light"],\n[data-md-color-scheme="default"]'
OS_LIGHT_SCOPE = ':root:not([data-theme="dark"])'
ALIAS_SCOPE = ":root,\n[data-theme],\n[data-md-color-scheme]"

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
COLOR_FN = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\(", re.I)
VAR_USE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*([,)])")
VAR_DEF = re.compile(r"(?<![\w-])(--[A-Za-z0-9_-]+)\s*:")
COMMENT = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


# ---------------------------------------------------------------- tokens

def load_tokens(path: Path = TOKENS) -> dict:
    return json.loads(path.read_text())


def release() -> str:
    """The newest theme-vN in theme/CHANGELOG.md; stamped into the generated files."""
    m = re.search(r"^## (theme-v\d+)\b", (THEME / "CHANGELOG.md").read_text(), re.M)
    return m.group(1) if m else "unreleased"


def themes(tokens: dict) -> list[str]:
    return [t["id"] for t in tokens["color"]["themes"]]


def themed_tokens(tokens: dict) -> list[dict]:
    return [t for fam in THEMED for t in tokens.get(fam, {}).get("tokens", [])]


def plain_tokens(tokens: dict) -> list[tuple[str, str]]:
    out = [(t["name"], str(t["value"])) for fam in PLAIN for t in tokens.get(fam, {}).get("tokens", [])]
    out += [(f"font-{k}", v) for k, v in tokens["type"]["families"].items()]
    return out


def value(token: dict, theme: str, ids: list[str]) -> str:
    v = token["value"]
    if isinstance(v, str):
        return v
    return v.get(theme, v[ids[0]])


def token_names(tokens: dict) -> set[str]:
    return {t["name"] for t in themed_tokens(tokens)} | {n for n, _ in plain_tokens(tokens)}


def resolved(tokens: dict) -> dict:
    """Tokens flattened per theme: {"themes": {"dark": {"canvas": "#000000", ...}, "light": {...}}}."""
    ids = themes(tokens)
    common = dict(plain_tokens(tokens))
    per = {i: {**{t["name"]: value(t, i, ids) for t in themed_tokens(tokens)}, **common} for i in ids}
    styles = {}
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            fam = s.get("family", group.get("family"))
            styles[s["name"]] = {k: v for k, v in s.items() if k not in ("name", "sample", "usage")} | {
                "fontFamily": tokens["type"]["families"].get(fam, fam)}
    return {
        "name": tokens.get("name", "Airframe"),
        "release": release(),
        "generated": "from airframe/tokens.json by scripts/airframe.py; do not edit",
        "defaultTheme": ids[0],
        "themeNames": {t["id"]: t["name"] for t in tokens["color"]["themes"]},
        "prefix": PREFIX,
        "themes": per,
        "typeStyles": styles,
        "aliases": ALIASES,
    }


def tokens_css(tokens: dict) -> str:
    ids = themes(tokens)
    dark, light = ids[0], ids[1]
    themed = themed_tokens(tokens)
    lines = [
        "/*",
        f"  Airframe {release()} tokens. Generated from airframe/tokens.json by scripts/airframe.py; do not edit.",
        "  Change a value in airframe/tokens.json, run `python3 scripts/airframe.py build`, and add a",
        "  theme/CHANGELOG.md entry. Tool repos vendor this file unmodified (scripts/sync-airframe.sh).",
        "",
        "  Contract: every token is --af-<name>; Night is `dark` (the default), Day is `light`, set with",
        "  data-theme on <html> or any element (the docs sites use data-md-color-scheme). Component",
        "  classes live in airframe-components.css. The brand yellow is never a status.",
        "*/",
        "",
    ]

    def block(selector: str, decls: list[str], indent: str = "") -> None:
        lines.append(f"{indent}{selector.replace(chr(10), chr(10) + indent)} {{")
        lines.extend(f"{indent}  {d}" for d in decls)
        lines.append(f"{indent}}}")

    block(DARK_SCOPE, ["color-scheme: dark;"] + [f"{PREFIX}{t['name']}: {value(t, dark, ids)};" for t in themed])
    light_decls = ["color-scheme: light;"] + [
        f"{PREFIX}{t['name']}: {value(t, light, ids)};" for t in themed if value(t, light, ids) != value(t, dark, ids)]
    lines.append("")
    lines.append("@media (prefers-color-scheme: light) {")
    block(OS_LIGHT_SCOPE, light_decls, indent="  ")
    lines.append("}")
    lines.append("")
    block(LIGHT_SCOPE, light_decls)
    lines.append("")
    block(":root", [f"{PREFIX}{n}: {v};" for n, v in plain_tokens(tokens)])
    lines.append("")
    lines.append("/* theme-v1 names, kept as aliases (re-declared in every theme scope so they follow it) */")
    names = token_names(tokens)
    for old, new in ALIASES.items():
        if new not in names:
            raise ValueError(f"alias --af-{old} points at unknown token {new}")
    block(ALIAS_SCOPE, [f"{PREFIX}{old}: var({PREFIX}{new});" for old, new in ALIASES.items()])
    return "\n".join(lines) + "\n"


def type_styles_css(tokens: dict) -> str:
    out = ["/* ===== type styles (from tokens.json): .af-type-<name> ===== */"]
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            fam = s.get("family", group.get("family"))
            px = lambda v: f"{v}px" if isinstance(v, (int, float)) else v  # noqa: E731
            decl = [f"font-family:var({PREFIX}font-{fam})"]
            if fam == "display":
                decl.append(f"font-stretch:var({PREFIX}display-stretch)")
            decl.append(f"font-size:{px(s['fontSize'])}")
            for key, prop in (("lineHeight", "line-height"), ("fontWeight", "font-weight"),
                              ("letterSpacing", "letter-spacing"), ("textTransform", "text-transform"),
                              ("fontStyle", "font-style")):
                if s.get(key) is not None:
                    decl.append(f"{prop}:{px(s[key]) if key == 'letterSpacing' else s[key]}")
            if fam == "mono" or s.get("tabular"):
                decl.append("font-variant-numeric:tabular-nums")
            out.append(f".af-type-{s['name']}{{{';'.join(decl)}}}")
    return "\n".join(out)


def components_css(tokens: dict) -> str:
    parts = [
        f"/* Airframe {release()} components: the af- classes. Generated from airframe/styles/ by scripts/airframe.py;",
        "   do not edit. Load after airframe.css. Reference and previews: airframe/components/, and the",
        "   gallery on https://sean-koval.github.io/agent-factory/airframe/ */",
        f"@import url('{FONTS_URL}');",
        type_styles_css(tokens),
    ]
    for name in STYLES:
        parts.append(f"/* ===== {name} ===== */\n" + (SRC / "styles" / name).read_text().strip())
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------- exports: Tailwind v4 and DTCG

def tailwind_css(tokens: dict) -> str:
    """A Tailwind CSS v4 theme (https://tailwindcss.com/docs/theme) over the --af- tokens.

    `@theme inline` makes every utility read the token variable itself, so bg-canvas follows data-theme.
    The color, font, radius and shadow namespaces are reset first: an Airframe project has no bg-blue-500,
    the same rule the CSS guard enforces (tokens only). Spacing keeps Tailwind's 4px scale, which is
    Airframe's: p-4 is space-16, gap-3 is space-12.
    """
    ids = themes(tokens)
    lines = [
        "/*",
        f"  Airframe {release()} for Tailwind CSS v4. Generated from airframe/tokens.json by scripts/airframe.py; do not edit.",
        "  Load after Tailwind and the tokens (airframe.css: the --af- tokens, Night and Day):",
        '    @import "tailwindcss";',
        '    @import "./airframe/airframe.css";',
        '    @import "./airframe/airframe-tailwind.css";',
        "  Utilities: bg-canvas, text-fg-muted, border-line, bg-brand text-on-brand, font-display, font-mono,",
        "  text-body, text-label (size, line-height, weight and tracking of the type style), rounded-card,",
        "  shadow-overlay. Tailwind's default color, font, radius and shadow scales are removed on purpose.",
        "*/",
        "@theme inline {",
        "  --color-*: initial;",
        "  --font-*: initial;",
        "  --radius-*: initial;",
        "  --shadow-*: initial;",
        "",
        "  /* colors: every Airframe color token, by its own name */",
    ]
    for t in tokens["color"]["tokens"]:
        lines.append(f"  --color-{t['name']}: var({PREFIX}{t['name']});")
    lines += ["", "  /* type: the three faces; text-<style> sets size, line-height, weight and tracking */"]
    for fam in tokens["type"]["families"]:
        if fam != "display":  # font-display is a custom utility below: it needs the width axis too
            lines.append(f"  --font-{fam}: var({PREFIX}font-{fam});")
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            name = s["name"]
            lines.append(f"  --text-{name}: {s['fontSize']};")
            if s.get("lineHeight") is not None:
                lines.append(f"  --text-{name}--line-height: {s['lineHeight']};")
            if s.get("fontWeight") is not None:
                lines.append(f"  --text-{name}--font-weight: {s['fontWeight']};")
            if s.get("letterSpacing") is not None:
                lines.append(f"  --text-{name}--letter-spacing: {s['letterSpacing']};")
    lines.append(f"  --tracking-label: var({PREFIX}label-track);")
    lines.append(f"  --tracking-display: var({PREFIX}display-track);")
    lines += ["", "  /* shape */"]
    for t in tokens["radius"]["tokens"]:
        short = t["name"].removeprefix("radius-")
        lines.append(f"  --radius-{short}: var({PREFIX}{t['name']});")
    for t in tokens["shadow"]["tokens"]:
        short = t["name"].removeprefix("shadow-")
        lines.append(f"  --shadow-{short}: var({PREFIX}{t['name']});")
    lines += ["", "  /* layout: max-w-page, h-header, h-row, h-row-compact, h-lane, h-span */"]
    layout = {t["name"] for t in tokens["layout"]["tokens"]}
    for name, tw in (("container-max", "--container-page"), ("header-h", "--spacing-header"), ("row-h", "--spacing-row"),
                     ("row-h-compact", "--spacing-row-compact"), ("lane-h", "--spacing-lane"), ("span-h", "--spacing-span")):
        if name in layout:
            lines.append(f"  {tw}: var({PREFIX}{name});")
    lines.append("}")
    lines += [
        "",
        "/* Archivo Expanded is Archivo's width axis at 125%: the display face always sets both. */",
        f"@utility font-display {{ font-family: var({PREFIX}font-display); font-stretch: var({PREFIX}display-stretch); }}",
        "",
        "/* The af- classes are unlayered, so a utility on the same element cannot override them; that is the",
        "   contract (compose af- classes as the component README shows, add utilities for layout around them).",
        "   Put Airframe's component CSS in a layer when a project must win with utilities:",
        "   @import \"./airframe/airframe-components.css\" layer(components); */",
    ]
    assert ids[0] == "dark"
    return "\n".join(lines) + "\n"


DTCG_EXT = "io.github.sean-koval.airframe"
_PX = re.compile(r"^(-?\d+(?:\.\d+)?)(px|rem)$")
_NUM = re.compile(r"^(-?\d+(?:\.\d+)?)(em|%)?$")
_RGBA = re.compile(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)$")
_SHADOW = re.compile(r"^(-?\d+)(?:px)?\s+(-?\d+)(?:px)?\s+(-?\d+)(?:px)?(?:\s+(-?\d+)(?:px)?)?\s+(.+)$")


def dtcg_color(css: str) -> dict:
    """A CSS color (hex or rgb[a]) as a DTCG color value (Color Module 2025.10, sRGB)."""
    m = _RGBA.match(css)
    if m:
        r, g, b = (int(m.group(i)) for i in (1, 2, 3))
        alpha = float(m.group(4)) if m.group(4) is not None else 1.0
    else:
        h = css.lstrip("#")
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    out = {"colorSpace": "srgb", "components": [round(r / 255, 4), round(g / 255, 4), round(b / 255, 4)],
           "hex": f"#{r:02X}{g:02X}{b:02X}"}
    if alpha != 1.0:
        out["alpha"] = round(alpha, 4)
    return out


def dtcg_dimension(css: str) -> dict | None:
    m = _PX.match(css.strip())
    return {"value": float(m.group(1)) if "." in m.group(1) else int(m.group(1)), "unit": m.group(2)} if m else None


def _dtcg_scalar(css: str, usage: str) -> dict:
    """px/rem become dimension; em and % become number with the unit kept in $extensions (DTCG has no em)."""
    d = dtcg_dimension(css)
    if d:
        return {"$type": "dimension", "$value": d, "$description": usage}
    m = _NUM.match(css.strip())
    if m:
        n = float(m.group(1)) if "." in m.group(1) else int(m.group(1))
        tok = {"$type": "number", "$value": n, "$description": usage}
        if m.group(2):
            tok["$extensions"] = {DTCG_EXT: {"unit": m.group(2), "css": css}}
        return tok
    raise ValueError(f"cannot express {css!r} as a DTCG value")


def dtcg_shadow(css: str) -> dict:
    m = _SHADOW.match(css.strip())
    if not m:
        raise ValueError(f"cannot parse shadow {css!r}")
    px = lambda v: {"value": int(v or 0), "unit": "px"}  # noqa: E731
    return {"color": dtcg_color(m.group(5).strip()), "offsetX": px(m.group(1)), "offsetY": px(m.group(2)),
            "blur": px(m.group(3)), "spread": px(m.group(4))}


def dtcg(tokens: dict, theme: str) -> dict:
    """One complete W3C Design Tokens file (Format Module 2025.10) for a theme.

    Groups: color, font (families and the display axis), type (typography composites), space, radius,
    shadow, layout, icon. Letter-spacing in em is converted to px for the typography composite (the spec
    allows px and rem only) and kept as written under $extensions. Themes are separate files because the
    core format has no modes; the Resolver Module that adds them is still a preview draft.
    """
    ids = themes(tokens)
    names = {t["id"]: t["name"] for t in tokens["color"]["themes"]}
    doc: dict = {
        "$description": (f"Airframe {release()}, {names[theme]} theme, in the Design Tokens Format Module 2025.10. "
                         "Generated from airframe/tokens.json by scripts/airframe.py; do not edit. Each token's "
                         "'css' extension names its CSS custom property or class."),
        "$extensions": {DTCG_EXT: {"theme": theme, "themeName": names[theme], "release": release(),
                                   "defaultTheme": ids[0], "prefix": PREFIX,
                                   "format": "https://www.designtokens.org/tr/drafts/format/"}},
    }
    css = lambda name: {DTCG_EXT: {"css": f"{PREFIX}{name}"}}  # noqa: E731
    doc["color"] = {"$type": "color"}
    for t in tokens["color"]["tokens"]:
        doc["color"][t["name"]] = {"$value": dtcg_color(value(t, theme, ids)), "$description": t["usage"],
                                   "$extensions": css(t["name"])}
    doc["font"] = {"$description": "Font families and the display axis settings."}
    for fam, stack in tokens["type"]["families"].items():
        doc["font"][fam] = {"$type": "fontFamily", "$value": [s.strip().strip('"') for s in stack.split(",")],
                            "$extensions": css(f"font-{fam}")}
    for t in tokens["font"]["tokens"]:
        if t["name"] == "display-weight":
            tok = {"$type": "fontWeight", "$value": int(t["value"]), "$description": t["usage"]}
        else:
            tok = _dtcg_scalar(t["value"], t["usage"])
        tok.setdefault("$extensions", {}).update(css(t["name"]))
        doc["font"][t["name"]] = tok
    doc["type"] = {"$type": "typography", "$description": "The type styles (.af-type-<name>)."}
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            fam = s.get("family", group.get("family"))
            size = dtcg_dimension(s["fontSize"])
            val: dict = {"fontFamily": "{font." + fam + "}", "fontSize": size,
                         "fontWeight": int(s.get("fontWeight", 400)), "lineHeight": float(s.get("lineHeight", 1))}
            ext = {"css": f".af-type-{s['name']}"}
            if s.get("letterSpacing") not in (None, "0"):
                m = _NUM.match(str(s["letterSpacing"]))
                if m and m.group(2) == "em" and size:
                    val["letterSpacing"] = {"value": round(float(m.group(1)) * size["value"], 3), "unit": "px"}
                    ext["letterSpacing"] = s["letterSpacing"]
            for k in ("textTransform", "fontStyle", "tabular"):
                if s.get(k):
                    ext[k] = s[k]
            doc["type"][s["name"]] = {"$value": val, "$description": s.get("usage", ""), "$extensions": {DTCG_EXT: ext}}
    for fam, group in (("spacing", "space"), ("radius", "radius"), ("layout", "layout"), ("icon", "icon")):
        doc[group] = {}
        for t in tokens[fam]["tokens"]:
            key = t["name"].removeprefix(f"{group}-") if group in ("space", "radius") else t["name"]
            tok = _dtcg_scalar(str(t["value"]), t.get("usage", ""))
            tok.setdefault("$extensions", {}).update(css(t["name"]))
            doc[group][key] = tok
    doc["shadow"] = {"$type": "shadow"}
    for t in tokens["shadow"]["tokens"]:
        doc["shadow"][t["name"].removeprefix("shadow-")] = {
            "$value": dtcg_shadow(value(t, theme, ids)), "$description": t["usage"], "$extensions": css(t["name"])}
    return doc


def outputs(tokens: dict | None = None) -> dict[Path, str]:
    tokens = tokens or load_tokens()
    dump = lambda d: json.dumps(d, indent=2, ensure_ascii=False) + "\n"  # noqa: E731
    return {
        THEME / "airframe.css": tokens_css(tokens),
        THEME / "airframe-components.css": components_css(tokens),
        THEME / "airframe-icons.svg": (SRC / "icons" / "airframe-icons.svg").read_text(),
        THEME / "airframe.js": HELPERS.read_text(),
        THEME / "airframe-tokens.json": dump(resolved(tokens)),
        THEME / "airframe-tailwind.css": tailwind_css(tokens),
        THEME / "airframe.tokens.json": dump(dtcg(tokens, "dark")),
        THEME / "airframe-day.tokens.json": dump(dtcg(tokens, "light")),
        THEME / "airframe-docs.css": docs_css(),
        THEME / "airframe-suite.html": (DOCS_SITE / "airframe-suite.html").read_text(),
    }


def docs_css() -> str:
    """The docs-site mapping, stamped with the release; the source is airframe/docs-site/airframe-docs.css."""
    src = (DOCS_SITE / "airframe-docs.css").read_text()
    head = (f"/* Airframe {release()} for the docs sites. Generated from airframe/docs-site/airframe-docs.css by "
            "scripts/airframe.py; do not edit. Load after airframe.css. */\n")
    return head + src


# ---------------------------------------------------------------- checks

def strip_css(text: str) -> str:
    return COMMENT.sub("", text)


def color_literals(text: str) -> list[str]:
    body = strip_css(HTML_COMMENT.sub("", text))
    return HEX.findall(body) + [m.group(0) for m in COLOR_FN.finditer(body)]


def defined_vars(*texts: str) -> set[str]:
    return {m.group(1) for t in texts for m in VAR_DEF.finditer(strip_css(t))}


def problems() -> list[str]:
    found: list[str] = []
    tokens = load_tokens()
    ids = themes(tokens)
    if ids[:2] != ["dark", "light"]:
        found.append(f"tokens.json: themes must be dark then light, got {ids}")
    for t in themed_tokens(tokens):
        v = t["value"]
        if not isinstance(v, dict) or any(i not in v for i in ids):
            found.append(f"tokens.json: {t['name']} needs a value for each theme {ids}")
        if not t.get("usage"):
            found.append(f"tokens.json: {t['name']} has no usage note")

    for path, text in outputs(tokens).items():
        if not path.exists() or path.read_text() != text:
            found.append(f"{path.relative_to(ROOT)} is out of date; run python3 scripts/airframe.py build")

    sources = (sorted((SRC / "styles").glob("*.css")) + sorted((SRC / "components").glob("*/preview.html"))
               + [DOCS_SITE / "airframe-docs.css", DOCS_SITE / "airframe-suite.html"])
    for path in sources:
        for lit in color_literals(path.read_text()):
            found.append(f"{path.relative_to(ROOT)}: color literal {lit}; use an Airframe token (var(--af-<name>))")

    found += registry_problems()

    # every var(--af-...) the theme files and previews use must be a token, an alias or a local variable
    css_files = [THEME / "airframe-components.css", THEME / "airframe-docs.css", THEME / "suite.css",
                 THEME / "airframe-tailwind.css"]
    texts = {p: p.read_text() for p in css_files + sources if p.exists()}
    known = {PREFIX + n for n in token_names(tokens)} | {PREFIX + a for a in ALIASES} | {"--af-product", "--af-tool"}
    known |= defined_vars(*texts.values())
    for path, text in texts.items():
        # a var() with a fallback is a customization hook (var(--af-list-time, 5.5em)); it needs no definition
        for name in sorted({m.group(1) for m in VAR_USE.finditer(strip_css(text)) if m.group(2) == ")"}):
            if name.startswith(PREFIX) and name not in known:
                found.append(f"{path.relative_to(ROOT)}: var({name}) is not an Airframe token")
            if not name.startswith(PREFIX) and path.suffix == ".css" and path.parent == THEME:
                if name not in known and not name.startswith("--md-"):
                    found.append(f"{path.relative_to(ROOT)}: var({name}) is neither --af- nor defined here")

    for comp in sorted(p for p in (SRC / "components").iterdir() if p.is_dir() and p.name != "Cover"):
        for need in ("README.md", "preview.html"):
            if not (comp / need).exists():
                found.append(f"{comp.relative_to(ROOT)}: missing {need}")
        prev = comp / "preview.html"
        if prev.exists() and not prev.read_text().startswith("<!-- @dsCard"):
            found.append(f"{prev.relative_to(ROOT)}: line 1 must be the <!-- @dsCard ... --> marker")
    return found


# ---------------------------------------------------------------- contrast (used by the tests)

def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------------------------------------------------------------- gallery

GROUPS = ("Foundations", "Cards", "Controls", "Navigation", "Patterns", "Alerts", "Governance", "Data", "Fleet", "Marketing")
MARKER = re.compile(r'^\s*<!--\s*@dsCard\b(.*?)-->')
ATTR = re.compile(r'([A-Za-z]+)(?:=(?:"([^"]*)"|(\S+)))?')


def parse_preview(src: str) -> dict:
    first, _, rest = src.partition("\n")
    m = MARKER.match(first)
    marker = {a[0]: a[1] or a[2] or True for a in ATTR.findall(m.group(1))} if m else {}
    doc = rest if m else src
    head = re.search(r"<head\b[^>]*>(.*?)</head>", doc, re.S | re.I)
    head_keep = ""
    if head:
        head_keep = re.sub(r"<meta\b[^>]*>|<title\b[^>]*>.*?</title>", "", head.group(1), flags=re.S | re.I).strip()
    body = re.search(r"<body\b([^>]*)>(.*)</body>", doc, re.S | re.I)
    return {"marker": marker, "head": head_keep,
            "attrs": body.group(1).strip() if body else "", "body": (body.group(2) if body else doc).strip()}


def summary(readme: Path) -> str:
    if not readme.exists():
        return ""
    for block in re.split(r"\n\s*\n", readme.read_text()):
        b = block.strip()
        if b and not b.startswith(("#", "```", "|", "<", "-")):
            plain = re.sub(r"\s+", " ", b)
            plain = re.sub(r"`([^`]*)`", r"\1", plain)
            plain = re.sub(r"\*\*([^*]*)\*\*", r"\1", plain)
            plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", plain)
            m = re.match(r"(.+?[.!?])(\s|$)", plain)
            return (m.group(1) if m else plain).strip()
    return ""


def components() -> list[dict]:
    items = []
    for comp in sorted(p for p in (SRC / "components").iterdir() if p.is_dir()):
        prev = comp / "preview.html"
        if not prev.exists():
            continue
        parts = parse_preview(prev.read_text())
        group = "Cover" if comp.name == "Cover" else parts["marker"].get("group", "Other")
        items.append({"name": comp.name, "group": group, "parts": parts,
                      "subtitle": parts["marker"].get("subtitle", ""), "summary": summary(comp / "README.md")})
    order = ["Cover", *GROUPS]
    return sorted(items, key=lambda i: (order.index(i["group"]) if i["group"] in order else 99, i["name"]))


THEME_HEAD = ("<script>(function(){var t=null;try{t=new URLSearchParams(location.search).get('theme')"
              "||localStorage.getItem('airframe-theme')}catch(e){}"
              "document.documentElement.setAttribute('data-theme',t==='light'?'light':'dark')})();</script>")
THEME_SWITCH = ('<div class="afg-seg" role="group" aria-label="Theme">'
                '<button type="button" data-afg-theme="dark" aria-pressed="false">Night</button>'
                '<button type="button" data-afg-theme="light" aria-pressed="false">Day</button></div>')
THEME_SCRIPT = ("<script>(function(){var r=document.documentElement;function sync(){var t=r.getAttribute('data-theme');"
                "document.querySelectorAll('[data-afg-theme]').forEach(function(b){b.setAttribute('aria-pressed',"
                "String(b.getAttribute('data-afg-theme')===t))})}sync();document.addEventListener('click',function(e){"
                "var b=e.target.closest&&e.target.closest('[data-afg-theme]');if(!b)return;var t=b.getAttribute("
                "'data-afg-theme');r.setAttribute('data-theme',t);try{localStorage.setItem('airframe-theme',t)}catch(x){}"
                "sync()})})();</script>")
GALLERY_CSS = """<style>
.afg-bar{position:fixed;right:var(--af-space-12);bottom:var(--af-space-12);z-index:2147483000;display:flex;align-items:center;gap:var(--af-space-8);padding:var(--af-space-4) var(--af-space-4) var(--af-space-4) var(--af-space-12);background:var(--af-overlay);border:1px solid var(--af-line);border-radius:var(--af-radius-card);box-shadow:var(--af-shadow-overlay);font-family:var(--af-font-mono);font-size:11px;letter-spacing:var(--af-label-track);text-transform:uppercase;color:var(--af-fg-subtle)}
.afg-bar a{color:var(--af-fg-muted);text-decoration:none}.afg-bar a:hover{color:var(--af-fg)}
.afg-seg{display:flex;gap:2px}
.afg-seg button{height:26px;padding:0 var(--af-space-8);border:1px solid transparent;border-radius:var(--af-radius-control);background:transparent;color:var(--af-fg-muted);font-family:var(--af-font-mono);font-weight:500;font-size:11px;letter-spacing:var(--af-label-track);text-transform:uppercase;cursor:pointer}
.afg-seg button:hover{color:var(--af-fg)}
.afg-seg button[aria-pressed="true"]{background:var(--af-selected);border-color:var(--af-line-strong);color:var(--af-fg)}
.afg-spacer{height:56px}
.afg-page{max-width:var(--af-container-max);margin:0 auto;padding:var(--af-space-48) var(--af-space-32) var(--af-space-64)}
.afg-head{display:flex;flex-direction:column;gap:var(--af-space-12);margin-bottom:var(--af-space-40)}
.afg-head h1{font-size:48px;line-height:1.02}
.afg-head p{margin:0;max-width:62ch;color:var(--af-fg-muted)}
.afg-head p a{color:var(--af-fg);text-decoration-color:var(--af-brand-line);text-underline-offset:.2em}
.afg-row{display:flex;justify-content:space-between;align-items:flex-start;gap:var(--af-space-16)}
.afg-jump{display:flex;flex-wrap:wrap;gap:var(--af-space-4) var(--af-space-16);margin-top:var(--af-space-8)}
.afg-jump a{color:var(--af-fg-muted);text-decoration:none;padding:var(--af-space-4) 0;border-bottom:2px solid transparent}
.afg-jump a:hover{color:var(--af-fg);border-bottom-color:var(--af-fg)}
.afg-group{margin-bottom:var(--af-space-28);scroll-margin-top:var(--af-space-16)}
.afg-group h2{margin:0 0 var(--af-space-12)}
.afg-list{list-style:none;margin:0;padding:0;background:var(--af-raised);border-radius:var(--af-radius-card)}
.afg-item{display:grid;grid-template-columns:minmax(140px,200px) minmax(0,1fr) auto;align-items:center;gap:var(--af-space-16);min-height:var(--af-row-h);padding:var(--af-space-4) var(--af-space-16);border-top:1px solid var(--af-line-subtle)}
.afg-item:first-child{border-top:0}
.afg-item__name{font-family:var(--af-font-mono);font-weight:500;font-size:13px;color:var(--af-fg);text-decoration:none}
.afg-item__name:hover{color:var(--af-brand-text)}
.afg-item__sub{font-size:13px;line-height:1.4;color:var(--af-fg-muted);min-width:0;overflow-wrap:anywhere}
.afg-item__go{display:flex;gap:var(--af-space-4)}
.afg-item__go .af-btn{text-decoration:none}
@media (max-width:760px){.afg-page{padding:var(--af-space-32) var(--af-space-16)}.afg-item{grid-template-columns:minmax(0,1fr) auto}.afg-item__sub{grid-column:1/-1}.afg-item__go{grid-row:1;grid-column:2}}
</style>"""


def _page(title: str, head: str, body: str, attrs: str = "") -> str:
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{THEME_HEAD}
<link rel="stylesheet" href="airframe.css">
<link rel="stylesheet" href="airframe-components.css">
{GALLERY_CSS}
{head}
</head>
<body{(' ' + attrs) if attrs else ''}>
{body}
{THEME_SCRIPT}
</body>
</html>
"""


def gallery(dest: Path) -> int:
    for path, text in outputs().items():
        if path.suffix == ".css" and path.read_text() != text:
            raise SystemExit("theme/ is out of date; run python3 scripts/airframe.py build first")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for f in ("airframe.css", "airframe-components.css", "airframe-icons.svg", "airframe.js"):
        shutil.copy(THEME / f, dest / f)
    items = components()
    for it in items:
        p = it["parts"]
        bar = (f'<div class="afg-spacer" aria-hidden="true"></div><nav class="afg-bar" aria-label="Preview">'
               f'<a href="index.html">All components</a><span title="{html.escape(it["subtitle"])}">{it["name"]}</span>'
               f'{THEME_SWITCH}</nav>')
        (dest / f"{it['name']}.html").write_text(_page(f"{it['name']} · Airframe", p["head"], p["body"] + "\n" + bar, p["attrs"]))
    sections, jumps = [], []
    slug = lambda g: re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")  # noqa: E731
    for group in dict.fromkeys(i["group"] for i in items):
        # one line per component: the name, what it is, and both themes; the long summary is the row's title
        rows = "\n".join(
            f'<li class="afg-item" title="{html.escape(i["summary"])}"><a class="afg-item__name" href="{i["name"]}.html">{i["name"]}</a>'
            f'<span class="afg-item__sub">{html.escape(i["subtitle"])}</span>'
            f'<span class="afg-item__go"><a class="af-btn af-btn--ghost af-btn--sm" href="{i["name"]}.html?theme=dark">Night</a>'
            f'<a class="af-btn af-btn--ghost af-btn--sm" href="{i["name"]}.html?theme=light">Day</a></span></li>'
            for i in items if i["group"] == group)
        count = sum(1 for i in items if i["group"] == group)
        sections.append(f'<section class="afg-group" id="{slug(group)}"><h2 class="af-lbl">{group}<span class="af-lbl__sub">{count}</span></h2>'
                        f'<ul class="afg-list">{rows}</ul></section>')
        jumps.append(f'<a href="#{slug(group)}">{group}<span class="af-lbl__sub">{count}</span></a>')
    n = sum(1 for i in items if i["name"] != "Cover")
    jump = f'<nav class="afg-jump af-lbl" aria-label="Groups">{"".join(jumps)}</nav>'
    body = f"""<main class="afg-page">
<header class="afg-head">
<div class="afg-row"><span class="af-lbl">Airframe<span class="af-lbl__sub">Component gallery</span></span>{THEME_SWITCH}</div>
<h1 class="af-display">Every part, both themes.</h1>
<p>{n} components built from <code>theme/airframe-components.css</code> on <code>theme/airframe.css</code>. Each one is rendered from its
<code>airframe/components/&lt;Name&gt;/preview.html</code>; its README next to it says when to use it. Back to <a href="../">the Airframe docs</a>.</p>
{jump}
</header>
{''.join(sections)}
</main>"""
    (dest / "index.html").write_text(_page("Airframe component gallery", "", body))
    return len(items)


# ---------------------------------------------------------------- reference pages

COLOR_GROUPS = (
    ("Ground", ("canvas", "surface", "raised", "overlay", "selected")),
    ("Lines", ("line-subtle", "line", "line-strong", "rule")),
    ("Text", ("fg", "fg-muted", "fg-subtle", "fg-dim")),
    ("Brand", ("brand", "brand-hover", "brand-wash", "on-brand", "brand-text", "brand-line", "focus")),
    ("Status", ("status-running", "status-queued", "status-approval", "status-failed", "status-denied",
                "on-status-denied", "status-off", "lamp-caution", "lamp-warning", "on-lamp")),
    ("Terminal and code", ("terminal-", "code-")),
    ("Traces, lanes and readouts", ("span-", "stage-", "readout-cell", "display-window", "dot-field")),
    ("Product hues", ("product-",)),
    ("Charts", ("chart-",)),
)


def _color_group(name: str) -> str:
    for title, keys in COLOR_GROUPS:
        if any(name == k or (k.endswith("-") and name.startswith(k)) for k in keys):
            return title
    return "Other"


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def pages(dest: Path, site: Path | None = None) -> list[Path]:
    """The snippets the docs include (dest) and, with `site` (docs/airframe), a page per component README and per guide chapter."""
    tokens = load_tokens()
    ids = themes(tokens)
    dest.mkdir(parents=True, exist_ok=True)
    written = []

    out = []
    groups: dict[str, list[dict]] = {}
    for t in tokens["color"]["tokens"]:
        groups.setdefault(_color_group(t["name"]), []).append(t)
    for title, _ in [*COLOR_GROUPS, ("Other", ())]:
        if title not in groups:
            continue
        out += [f"### {title}", "", "| | Token | Night | Day | Use |", "| --- | --- | --- | --- | --- |"]
        for t in groups[title]:
            sw = f'<span class="af-swatch" style="background: var({PREFIX}{t["name"]})"></span>'
            out.append(f"| {sw} | `{PREFIX}{t['name']}` | `{value(t, ids[0], ids)}` | `{value(t, ids[1], ids)}` | {_cell(t['usage'])} |")
        out.append("")
    (dest / "airframe-colors.md").write_text("\n".join(out))
    written.append(dest / "airframe-colors.md")

    out = ["| Style | Family | Size / line | Weight | Use |", "| --- | --- | --- | --- | --- |"]
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            fam = s.get("family", group.get("family"))
            sample = html.escape(s.get("sample") or s["name"])
            stretch = f" font-stretch: var({PREFIX}display-stretch);" if fam == "display" else ""
            size = s["fontSize"] if isinstance(s["fontSize"], str) else f"{s['fontSize']}px"
            preview = (f'<span class="af-type-sample" style="font-family: var({PREFIX}font-{fam});{stretch} '
                       f'font-weight: {s.get("fontWeight", 400)}; font-size: min({size}, 28px);'
                       f'{" text-transform: uppercase; letter-spacing: " + str(s["letterSpacing"]) + ";" if s.get("textTransform") == "uppercase" else ""}">{sample}</span>')
            out.append(f"| {preview}<br>`.af-type-{s['name']}` | {fam} | {size} / {s.get('lineHeight', '')} | "
                       f"{s.get('fontWeight', '')} | {_cell(s.get('usage', ''))} |")
    out += ["", "| Family token | Stack |", "| --- | --- |"]
    out += [f"| `{PREFIX}font-{k}` | `{_cell(v)}` |" for k, v in tokens["type"]["families"].items()]
    out += ["", "| Token | Value | Use |", "| --- | --- | --- |"]
    out += [f"| `{PREFIX}{t['name']}` | `{t['value']}` | {_cell(t.get('usage', ''))} |" for t in tokens["font"]["tokens"]]
    (dest / "airframe-type.md").write_text("\n".join(out) + "\n")
    written.append(dest / "airframe-type.md")

    out = ["| Token | Value | Use |", "| --- | --- | --- |"]
    for fam in ("spacing", "radius", "layout", "icon"):
        for t in tokens[fam]["tokens"]:
            out.append(f"| `{PREFIX}{t['name']}` | `{t['value']}` | {_cell(t.get('usage', ''))} |")
    for t in tokens["shadow"]["tokens"]:
        out.append(f"| `{PREFIX}{t['name']}` | `{value(t, ids[0], ids)}` (Night) | {_cell(t.get('usage', ''))} |")
    (dest / "airframe-shape.md").write_text("\n".join(out) + "\n")
    written.append(dest / "airframe-shape.md")

    # The Components page: a card per component, grouped, each with its Night thumbnail (docs/assets/airframe/<Name>.png,
    # made by scripts/captures.py airframe), the group, the preview's one-line subtitle, and the two theme links.
    # Paths are relative to docs/airframe/, where components.md sits; the docs build rewrites them per page.
    out = []
    items = [it for it in components() if it["name"] != "Cover"]
    for group in dict.fromkeys(i["group"] for i in items):
        out += [f"### {group}", "", '<div class="af-comps">']
        for it in (i for i in items if i["group"] == group):
            n = it["name"]
            thumb = THUMBS / f"{n}.png"
            pic = (f'<img src="../assets/airframe/{n}.png" alt="{html.escape(n)} preview, Night" loading="lazy" width="800" height="500">'
                   if thumb.exists() else '<span class="af-comp__blank">No thumbnail yet</span>')
            out.append(f'<a class="af-comp" href="components/{n}/" title="{html.escape(it["summary"])}">'
                       f'<span class="af-comp__pic">{pic}</span>'
                       f'<span class="af-comp__head"><b>{n}</b><span class="af-comp__group">{html.escape(group)}</span></span>'
                       f'<span class="af-comp__sub">{html.escape(it["subtitle"])}</span>'
                       f'<span class="af-comp__go"><span>Night</span><span>Day</span></span></a>')
        out += ["</div>", ""]
    (dest / "airframe-components.md").write_text("\n".join(out))
    written.append(dest / "airframe-components.md")

    if site is not None:
        written += component_pages(site / "components")
        written += guide_pages(site / "guide")

    index = json.loads((SRC / "icons" / "icons.json").read_text())
    cells = []
    for name, paths in index.items():
        cells.append(f'<figure class="af-icon"><svg viewBox="0 0 20 20" aria-hidden="true">{paths}</svg>'
                     f'<figcaption>{html.escape(name)}</figcaption></figure>')
    (dest / "airframe-icons.md").write_text('<div class="af-icons">\n' + "\n".join(cells) + "\n</div>\n")
    written.append(dest / "airframe-icons.md")

    # the registry page's pinned install commands name the newest release, like the header badge
    tag = release()
    (dest / "airframe-install.md").write_text(
        "```sh\n"
        f"npx shadcn@latest add {REGISTRY_REPO}/airframe#{tag}\n"
        f"npx shadcn@latest add {REGISTRY_REPO}/skill#{tag}\n"
        f"npx shadcn@latest list {REGISTRY_REPO}\n"
        "```\n\n"
        "!!! note \"A `#ref` pins one item\"\n"
        f"    The CLI does not carry the ref to that item's dependencies, which it reads from `main`, so `button#{tag}` installs "
        "that tag's contract but the current `airframe` files. Pin the whole set by naming every item in one command, or "
        "install from the site, where each release's items are built together.\n")
    written.append(dest / "airframe-install.md")
    return written


# ---------------------------------------------------------------- component and guide pages

GENERATED = "<!-- Generated by scripts/airframe.py pages from {src}; edit that file, not this one. -->"
# The order a reader wants: what it is, when to use it, do, don't, anything else, then what you provide and the markup last.
SECTION_ORDER = ("When to use", "Do", "Don't", "*", "You provide", "Markup")
GUIDE_TITLES = {"brand": "Brand book", "Status": "Status", "Data": "Data", "Products": "Products"}


def _sections(md: str) -> tuple[str, list[tuple[str, str]]]:
    """Split a README into (lead text before the first ##, [(heading, body)…]); the top-level # title is dropped."""
    md = re.sub(r"\A#\s[^\n]*\n", "", md.strip() + "\n", count=1)
    parts = re.split(r"(?m)^##\s+(.+)$", md)
    lead = parts[0].strip()
    return lead, [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def _ordered(sections: list[tuple[str, str]]) -> list[tuple[str, str]]:
    named = [n for n in SECTION_ORDER if n != "*"]
    out = []
    for key in SECTION_ORDER:
        if key == "*":
            out += [s for s in sections if s[0] not in named]
        else:
            out += [s for s in sections if s[0] == key]
    return out


def _indent(text: str, n: int = 4) -> str:
    return "\n".join((" " * n + line) if line.strip() else "" for line in text.splitlines())


def component_page(it: dict, height: int) -> str:
    n = it["name"]
    readme = SRC / "components" / n / "README.md"
    lead, sections = _sections(readme.read_text()) if readme.exists() else ("", [])
    rel = f"airframe/components/{n}/README.md"
    out = ["---", f"title: {n}", "---", "", GENERATED.format(src=rel), "",
           f'<span class="af-eyebrow">{html.escape(it["group"])}</span>', "", f"# {n}", ""]
    if lead:
        out += [lead, ""]
    out += [f'<iframe class="af-preview" src="../gallery/{n}.html?theme=dark" title="{html.escape(n)} preview" loading="lazy" '
            f'style="height: {min(max(height, 240), 720)}px"></iframe>', "",
            f'[Night](../gallery/{n}.html?theme=dark){{ .md-button .md-button--primary }} [Day](../gallery/{n}.html?theme=light){{ .md-button }} '
            f'[Source](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/components/{n}){{ .md-button }}', ""]
    for heading, body in _ordered(sections):
        if heading == "Markup":
            out += ['??? note "Markup"', "", _indent(body), ""]
        else:
            out += [f"## {heading}", "", body, ""]
    return "\n".join(out).rstrip() + "\n"


def component_pages(dest: Path) -> list[Path]:
    """One docs page per component, from its README, with the Night preview framed at the top and the markup last."""
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for it in components():
        if it["name"] == "Cover":
            continue
        h = it["parts"]["marker"].get("height", 480)
        try:
            h = int(h)
        except (TypeError, ValueError):
            h = 480
        path = dest / f"{it['name']}.md"
        path.write_text(component_page(it, h))
        written.append(path)
    return written


def guide_pages(dest: Path) -> list[Path]:
    """The brand book and its chapters (airframe/guide/*.md) as docs pages, unchanged but for a provenance line."""
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for src in sorted((SRC / "guide").glob("*.md")):
        text = src.read_text()
        title = GUIDE_TITLES.get(src.stem, src.stem)
        if src.stem == "brand":
            text = re.sub(r"\A#\s[^\n]*\n", "# Brand book\n", text, count=1)
        path = dest / f"{src.stem.lower()}.md"
        path.write_text(f"---\ntitle: {title}\n---\n\n{GENERATED.format(src=f'airframe/guide/{src.name}')}\n\n{text}")
        written.append(path)
    return written


# ---------------------------------------------------------------- registry (shadcn-compatible)

REGISTRY = ROOT / "registry.json"
REGISTRY_URL = "https://sean-koval.github.io/agent-factory/r"
REGISTRY_REPO = "Sean-Koval/agent-factory"   # the GitHub source-registry address of this repo
ITEM_SCHEMA = "https://ui.shadcn.com/schema/registry-item.json"
# https://ui.shadcn.com/schema/registry-item.json: the item types, and the file types (no font)
ITEM_TYPES = ("registry:lib", "registry:block", "registry:component", "registry:ui", "registry:hook", "registry:theme",
              "registry:page", "registry:file", "registry:style", "registry:base", "registry:font", "registry:item")
FILE_TYPES = tuple(t for t in ITEM_TYPES if t != "registry:font")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def registry() -> dict:
    return json.loads(REGISTRY.read_text())


def registry_problems() -> list[str]:
    """registry.json obeys the shadcn registry schema, and every file it names exists.

    Airframe items are "universal" items (type registry:item, every file with an explicit `~/` target),
    so they install into any project: no components.json, Tailwind or React needed.
    """
    found: list[str] = []
    if not REGISTRY.exists():
        return ["registry.json is missing"]
    try:
        reg = registry()
    except json.JSONDecodeError as e:
        return [f"registry.json: {e}"]
    for key in ("$schema", "name", "homepage", "items"):
        if key not in reg:
            found.append(f"registry.json: missing {key}")
    names = [it.get("name") for it in reg.get("items", [])]
    if len(set(names)) != len(names):
        found.append("registry.json: item names must be unique")
    for it in reg.get("items", []):
        where = f"registry.json: item {it.get('name')!r}"
        if not NAME_RE.match(str(it.get("name", ""))):
            found.append(f"{where}: name must be lowercase letters, digits and dashes")
        if it.get("type") not in ITEM_TYPES:
            found.append(f"{where}: type {it.get('type')!r} is not a registry item type")
        if not it.get("title") or not it.get("description"):
            found.append(f"{where}: needs a title and a description (agents and the CLI search them)")
        if not it.get("files"):
            found.append(f"{where}: needs at least one file")
        for f in it.get("files", []):
            if f.get("type") not in FILE_TYPES:
                found.append(f"{where}: file {f.get('path')!r} has type {f.get('type')!r}")
            if not f.get("path") or not (ROOT / f["path"]).is_file():
                found.append(f"{where}: file {f.get('path')!r} does not exist")
            if f.get("type") in ("registry:file", "registry:page", "registry:item") or it.get("type") == "registry:item":
                if not str(f.get("target", "")).startswith("~/"):
                    found.append(f"{where}: file {f.get('path')!r} needs a target starting with ~/ (universal item)")
        for dep in it.get("registryDependencies", []):
            # a bare name means a shadcn/ui item to the CLI, on every route; items here are addressed by repo
            if dep.startswith(f"{REGISTRY_REPO}/"):
                if dep.split("#")[0].removeprefix(f"{REGISTRY_REPO}/") not in names:
                    found.append(f"{where}: registryDependencies {dep!r} is not an item in this registry")
            elif not dep.startswith(("https://", "http://", "@")):
                found.append(f"{where}: registryDependencies {dep!r} must be {REGISTRY_REPO}/<item>, a URL or @namespace/<item>")
    return found


def registry_items(base_url: str = REGISTRY_URL) -> dict[str, dict]:
    """Each item with its files' content inlined, as `shadcn build` would write them to public/r/.

    Dependencies on this registry's own items (`Sean-Koval/agent-factory/<item>` in registry.json, which is
    what the GitHub route needs) are rewritten to the item's URL on the docs site, so a URL install stays
    on the site. The CLI treats a bare name as a shadcn/ui item on every route, so the source never uses one.
    """
    reg = registry()
    names = {it["name"] for it in reg["items"]}
    prefix = f"{REGISTRY_REPO}/"
    out = {}
    for it in reg["items"]:
        item = {"$schema": ITEM_SCHEMA, **it}
        item["files"] = [{**f, "content": (ROOT / f["path"]).read_text()} for f in it["files"]]
        if it.get("registryDependencies"):
            item["registryDependencies"] = [
                f"{base_url}/{d.removeprefix(prefix).split('#')[0]}.json"
                if d.startswith(prefix) and d.removeprefix(prefix).split("#")[0] in names else d
                for d in it["registryDependencies"]]
        item.setdefault("meta", {})["release"] = release()
        out[it["name"]] = item
    return out


def registry_build(dest: Path, base_url: str = REGISTRY_URL) -> list[Path]:
    found = registry_problems()
    if found:
        raise SystemExit("\n".join(f"airframe: {f}" for f in found))
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    items = registry_items(base_url)
    for name, item in items.items():
        p = dest / f"{name}.json"
        p.write_text(json.dumps(item, indent=2, ensure_ascii=False) + "\n")
        written.append(p)
    reg = registry()
    index = {**reg, "items": [{k: v for k, v in it.items() if k != "files"} | {"files": [
        {k: v for k, v in f.items() if k != "content"} for f in it["files"]]} for it in reg["items"]]}
    (dest / "registry.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    written.append(dest / "registry.json")
    return written


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("check")
    g = sub.add_parser("gallery")
    g.add_argument("dest", type=Path)
    p = sub.add_parser("pages")
    p.add_argument("dest", type=Path)
    p.add_argument("--site", type=Path, help="docs/airframe: also write components/<Name>.md and guide/*.md there")
    r = sub.add_parser("registry")
    r.add_argument("dest", type=Path)
    r.add_argument("--base-url", default=REGISTRY_URL, help="where DIR will be served (for registryDependencies)")
    args = ap.parse_args(argv)

    if args.cmd == "build":
        for path, text in outputs().items():
            changed = not path.exists() or path.read_text() != text
            path.write_text(text)
            print(f"{'updated  ' if changed else 'unchanged'} {path.relative_to(ROOT)}")
        return 0
    if args.cmd == "check":
        found = problems()
        for f in found:
            print(f"airframe: {f}", file=sys.stderr)
        if not found:
            print("airframe: theme/ matches airframe/; sources use tokens only")
        return 1 if found else 0
    if args.cmd == "gallery":
        n = gallery(args.dest)
        print(f"airframe: {n} previews + index.html in {args.dest}")
        return 0
    if args.cmd == "pages":
        for path in pages(args.dest, args.site):
            print(f"airframe: wrote {path}")
        return 0
    if args.cmd == "registry":
        written = registry_build(args.dest, args.base_url.rstrip("/"))
        print(f"airframe: {len(written) - 1} registry items + registry.json in {args.dest}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
