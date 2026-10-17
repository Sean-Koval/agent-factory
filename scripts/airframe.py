#!/usr/bin/env python3
"""Airframe build: airframe/ is the source, theme/ is what the sites and the tool repos load.

    python3 scripts/airframe.py build          # regenerate the theme/ files below from airframe/
    python3 scripts/airframe.py check          # CI: theme/ is up to date and the sources obey the rules
    python3 scripts/airframe.py gallery DIR    # component previews in Night and Day (the docs site's gallery)
    python3 scripts/airframe.py pages DIR      # reference tables (tokens, components, icons) as Markdown snippets

Generated (never edit by hand):

    theme/airframe.css             every token as --af-<name>, both themes, plus the theme-v1 names as aliases
    theme/airframe-components.css  the af- component classes: fonts, type styles, base, core, viz
    theme/airframe-icons.svg       the icon sprite (<use href="airframe-icons.svg#af-agent">)
    theme/airframe-tokens.json     tokens resolved per theme, for scripts (diagrams, decks, tests)

Hand-written in theme/: airframe-docs.css (the docs-site mapping), suite.css, CHANGELOG.md.
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
STYLES = ("base.css", "core.css", "viz.css")
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


def outputs(tokens: dict | None = None) -> dict[Path, str]:
    tokens = tokens or load_tokens()
    return {
        THEME / "airframe.css": tokens_css(tokens),
        THEME / "airframe-components.css": components_css(tokens),
        THEME / "airframe-icons.svg": (SRC / "icons" / "airframe-icons.svg").read_text(),
        THEME / "airframe-tokens.json": json.dumps(resolved(tokens), indent=2, ensure_ascii=False) + "\n",
    }


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

    sources = sorted((SRC / "styles").glob("*.css")) + sorted((SRC / "components").glob("*/preview.html"))
    for path in sources:
        for lit in color_literals(path.read_text()):
            found.append(f"{path.relative_to(ROOT)}: color literal {lit}; use an Airframe token (var(--af-<name>))")

    # every var(--af-...) the theme files and previews use must be a token, an alias or a local variable
    css_files = [THEME / "airframe-components.css", THEME / "airframe-docs.css", THEME / "suite.css"]
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

GROUPS = ("Foundations", "Cards", "Controls", "Navigation", "Alerts", "Governance", "Data", "Fleet", "Marketing")
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
.afg-group{margin-bottom:var(--af-space-28)}
.afg-group h2{margin:0 0 var(--af-space-12)}
.afg-list{list-style:none;margin:0;padding:0;background:var(--af-raised);border-radius:var(--af-radius-card)}
.afg-item{display:grid;grid-template-columns:minmax(140px,200px) minmax(0,1fr) auto;align-items:center;gap:var(--af-space-16);min-height:var(--af-row-h);padding:var(--af-space-8) var(--af-space-16);border-top:1px solid var(--af-line-subtle)}
.afg-item:first-child{border-top:0}
.afg-item__name{font-family:var(--af-font-mono);font-weight:500;font-size:13px;color:var(--af-fg);text-decoration:none}
.afg-item__name:hover{color:var(--af-brand-text)}
.afg-item__text{display:flex;flex-direction:column;gap:2px;min-width:0}
.afg-item__sub{font-size:13px;color:var(--af-fg-muted)}
.afg-item__sum{font-size:12px;color:var(--af-fg-subtle)}
.afg-item__go{display:flex;gap:var(--af-space-4)}
.afg-item__go .af-btn{text-decoration:none}
@media (max-width:760px){.afg-page{padding:var(--af-space-32) var(--af-space-16)}.afg-item{grid-template-columns:minmax(0,1fr) auto}.afg-item__text{grid-column:1/-1}.afg-item__go{grid-row:1;grid-column:2}}
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
    for f in ("airframe.css", "airframe-components.css", "airframe-icons.svg"):
        shutil.copy(THEME / f, dest / f)
    items = components()
    for it in items:
        p = it["parts"]
        bar = (f'<div class="afg-spacer" aria-hidden="true"></div><nav class="afg-bar" aria-label="Preview">'
               f'<a href="index.html">All components</a><span title="{html.escape(it["subtitle"])}">{it["name"]}</span>'
               f'{THEME_SWITCH}</nav>')
        (dest / f"{it['name']}.html").write_text(_page(f"{it['name']} · Airframe", p["head"], p["body"] + "\n" + bar, p["attrs"]))
    sections = []
    for group in dict.fromkeys(i["group"] for i in items):
        rows = "\n".join(
            f'<li class="afg-item"><a class="afg-item__name" href="{i["name"]}.html">{i["name"]}</a>'
            f'<span class="afg-item__text"><span class="afg-item__sub">{html.escape(i["subtitle"])}</span>'
            f'<span class="afg-item__sum">{html.escape(i["summary"])}</span></span>'
            f'<span class="afg-item__go"><a class="af-btn af-btn--ghost af-btn--sm" href="{i["name"]}.html?theme=dark">Night</a>'
            f'<a class="af-btn af-btn--ghost af-btn--sm" href="{i["name"]}.html?theme=light">Day</a></span></li>'
            for i in items if i["group"] == group)
        count = sum(1 for i in items if i["group"] == group)
        sections.append(f'<section class="afg-group"><h2 class="af-lbl">{group}<span class="af-lbl__sub">{count}</span></h2>'
                        f'<ul class="afg-list">{rows}</ul></section>')
    n = sum(1 for i in items if i["name"] != "Cover")
    body = f"""<main class="afg-page">
<header class="afg-head">
<div class="afg-row"><span class="af-lbl">Airframe<span class="af-lbl__sub">Component gallery</span></span>{THEME_SWITCH}</div>
<h1 class="af-display">Every part, both themes.</h1>
<p>{n} components built from <code>theme/airframe-components.css</code> on <code>theme/airframe.css</code>. Each one is rendered from its
<code>airframe/components/&lt;Name&gt;/preview.html</code>; its README next to it says when to use it. Back to <a href="../">the Airframe docs</a>.</p>
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


def pages(dest: Path) -> list[Path]:
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

    out = ["| Component | Group | What it is | Preview |", "| --- | --- | --- | --- |"]
    for it in components():
        if it["name"] == "Cover":
            continue
        src = f"https://github.com/Sean-Koval/agent-factory/tree/main/airframe/components/{it['name']}"
        out.append(f"| [{it['name']}]({src}) | {it['group']} | {_cell(it['summary'])} | "
                   f"[Night](../gallery/{it['name']}.html?theme=dark) · [Day](../gallery/{it['name']}.html?theme=light) |")
    (dest / "airframe-components.md").write_text("\n".join(out) + "\n")
    written.append(dest / "airframe-components.md")

    index = json.loads((SRC / "icons" / "icons.json").read_text())
    cells = []
    for name, paths in index.items():
        cells.append(f'<figure class="af-icon"><svg viewBox="0 0 20 20" aria-hidden="true">{paths}</svg>'
                     f'<figcaption>{html.escape(name)}</figcaption></figure>')
    (dest / "airframe-icons.md").write_text('<div class="af-icons">\n' + "\n".join(cells) + "\n</div>\n")
    written.append(dest / "airframe-icons.md")
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
        for path in pages(args.dest):
            print(f"airframe: wrote {path}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
