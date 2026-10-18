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
            self.assertGreaterEqual(n, 30)
            index = (Path(tmp) / "gallery" / "index.html").read_text()
            self.assertIn('href="Status.html"', index)
            self.assertIn(">Patterns<", index)
            self.assertLess(index.index(">Patterns<"), index.index(">Governance<"), "patterns are listed with the other groups")
            self.assertTrue((Path(tmp) / "gallery" / "airframe-components.css").exists())
            self.assertTrue((Path(tmp) / "gallery" / "airframe.js").exists(), "the gallery serves the helpers for the live previews")
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


SYSTEM_COLORS = {"Canvas", "CanvasText", "LinkText", "VisitedText", "ActiveText", "ButtonFace", "ButtonText",
                 "ButtonBorder", "Field", "FieldText", "Highlight", "HighlightText", "SelectedItem", "SelectedItemText",
                 "Mark", "MarkText", "GrayText", "AccentColor", "AccentColorText"}


def forced_block(css: str) -> str:
    """The body of the stylesheet's @media (forced-colors: active) block, or '' when it has none."""
    start = css.find("@media (forced-colors: active){")
    if start < 0:
        return ""
    i, depth = css.index("{", start), 0
    for j in range(i, len(css)):
        depth += {"{": 1, "}": -1}.get(css[j], 0)
        if depth == 0:
            return css[i + 1 : j]
    raise AssertionError("unbalanced forced-colors block")


class ForcedColorsTests(unittest.TestCase):
    """Windows Contrast Themes replace colors and drop box-shadows; statuses must keep their shape and edges there."""

    def test_every_stylesheet_has_a_forced_colors_block_of_system_colors_only(self):
        for name in af.STYLES:
            body = forced_block((af.SRC / "styles" / name).read_text())
            self.assertTrue(body, f"{name} has no @media (forced-colors: active) block")
            self.assertNotIn("var(", body, f"{name}: tokens are replaced in forced colors; use system colors")
            self.assertNotRegex(body, r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", name)
            for value in re.findall(r"(?:background|color|outline|border(?:-[a-z]+)?):([^;}]*)", body):
                words = {w for w in re.findall(r"[A-Za-z]+", value)} - {"solid", "dashed", "none", "transparent", "px"}
                self.assertLessEqual(words, SYSTEM_COLORS | {"left", "style", "width"}, f"{name}: {value}")

    def test_status_marks_and_lit_edges_survive(self):
        base = forced_block((af.SRC / "styles" / "base.css").read_text())
        viz = forced_block((af.SRC / "styles" / "viz.css").read_text())
        self.assertIn(".af-status__mark{background:CanvasText}", base)
        self.assertRegex(base, r"\.af-card--lit\{outline")
        for cls in (".af-stand__mark", ".af-lane-mark--fail", ".af-lane-mark--deny"):
            self.assertIn(cls, viz)
        core = forced_block((af.SRC / "styles" / "core.css").read_text())
        self.assertIn(".af-avatar--agent::before{background:CanvasText}", core, "the hexagon keeps its edge")
        agents = forced_block((af.SRC / "styles" / "agents.css").read_text())
        self.assertRegex(agents, r"\.af-diff__line--add \.af-diff__s.*border-left:2px solid CanvasText", "diff gutter bars survive")
        patterns = forced_block((af.SRC / "styles" / "patterns.css").read_text())
        self.assertRegex(patterns, r"\.af-toast,\.af-dialog,\.af-drawer\{outline")
        for name in af.STYLES:
            self.assertNotIn("forced-color-adjust", (af.SRC / "styles" / name).read_text(), name)

    def test_diffs_are_greyscale_and_chips_are_not_pills(self):
        agents = af.strip_css((af.SRC / "styles" / "agents.css").read_text())
        diff = "\n".join(line for line in agents.splitlines() if ".af-diff" in line or ".af-comment" in line)
        self.assertNotIn("status-approval", diff.replace("af-diff__hh>.af-status", ""))
        self.assertNotIn("status-denied", diff)
        self.assertNotIn("product-", diff)
        self.assertNotIn("brand", diff)
        css = "\n".join(af.strip_css((af.SRC / "styles" / n).read_text()) for n in af.STYLES)
        for cls in ("af-chip", "af-obj", "af-tag"):
            rule = re.search(rf"^\.{cls}\{{([^}}]*)\}}", css, re.M)
            self.assertIsNotNone(rule, cls)
            self.assertIn("radius-control", rule.group(1), f".{cls} keeps the 2px radius; there are no pills")


class ExportTests(unittest.TestCase):
    """The Tailwind theme and the DTCG files say exactly what tokens.json says."""

    def test_tailwind_theme_covers_every_token_and_resets_the_defaults(self):
        css = af.tailwind_css(TOKENS)
        self.assertIn("@theme inline {", css)
        for ns in ("color", "font", "radius", "shadow"):
            self.assertIn(f"--{ns}-*: initial;", css, ns)
        for t in TOKENS["color"]["tokens"]:
            self.assertIn(f"--color-{t['name']}: var(--af-{t['name']});", css, t["name"])
        for group in TOKENS["type"]["groups"]:
            for st in group["styles"]:
                self.assertIn(f"--text-{st['name']}: {st['fontSize']};", css, st["name"])
        self.assertIn("@utility font-display { font-family: var(--af-font-display); font-stretch: var(--af-display-stretch); }", css)
        self.assertEqual(af.color_literals(css), [], "the Tailwind theme must reference tokens, never values")
        self.assertNotIn("*/ */", css)  # the header is one comment; a nested close would break the file

    def test_dtcg_files_are_complete_and_typed(self):
        for theme in ("dark", "light"):
            doc = af.dtcg(TOKENS, theme)
            self.assertEqual(doc["$extensions"][af.DTCG_EXT]["theme"], theme)
            for t in TOKENS["color"]["tokens"]:
                tok = doc["color"][t["name"]]
                self.assertEqual(tok["$value"]["colorSpace"], "srgb", t["name"])
                self.assertEqual(tok["$value"]["hex"], af.dtcg_color(t["value"][theme])["hex"])
                self.assertEqual(tok["$extensions"][af.DTCG_EXT]["css"], f"--af-{t['name']}")
            for group in TOKENS["type"]["groups"]:
                for st in group["styles"]:
                    self.assertIn(st["name"], doc["type"], st["name"])
            for name, node in doc.items():
                if name.startswith("$"):
                    continue
                for key, tok in node.items():
                    if key.startswith("$"):
                        continue
                    self.assertIn("$value", tok, f"{name}.{key}")
                    self.assertTrue("$type" in tok or "$type" in node, f"{name}.{key} has no type")
        self.assertEqual(af.dtcg_color("rgba(255,196,0,0.12)"), {"colorSpace": "srgb", "components": [1.0, 0.7686, 0.0],
                                                                 "hex": "#FFC400", "alpha": 0.12})
        self.assertEqual(af.dtcg_dimension("2px"), {"value": 2, "unit": "px"})
        self.assertIsNone(af.dtcg_dimension("50%"))
        self.assertEqual(af.dtcg(TOKENS, "light")["color"]["canvas"]["$value"]["hex"], TOKENS["color"]["tokens"][0]["value"]["light"].upper())


class RegistryTests(unittest.TestCase):
    """registry.json obeys the shadcn schema, builds, and ships what the tool repos vendor."""

    def test_registry_is_valid(self):
        self.assertEqual(af.registry_problems(), [])
        self.assertEqual(af.registry()["name"], "airframe")

    def test_registry_builds_with_content_and_absolute_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            written = af.registry_build(Path(tmp), "https://example.test/r")
            names = {p.name for p in written}
            self.assertIn("registry.json", names)
            for item in af.registry()["items"]:
                self.assertIn(f"{item['name']}.json", names)
            import json
            button = json.loads((Path(tmp) / "button.json").read_text())
            self.assertEqual(button["$schema"], af.ITEM_SCHEMA)
            self.assertEqual(button["registryDependencies"], ["https://example.test/r/airframe.json"])
            self.assertIn("af-btn--primary", button["files"][0]["content"])
            airframe = json.loads((Path(tmp) / "airframe.json").read_text())
            shipped = {f["target"]: f["content"] for f in airframe["files"]}
            # the registry ships the published files unmodified (forced-colors blocks included)
            for name in ("airframe.css", "airframe-components.css", "airframe-icons.svg"):
                self.assertEqual(shipped[f"~/airframe/{name}"], (af.THEME / name).read_text(), name)
            index = json.loads((Path(tmp) / "registry.json").read_text())
            self.assertNotIn("content", json.dumps(index["files"] if "files" in index else index["items"]))

    def test_registry_items_are_universal(self):
        for item in af.registry()["items"]:
            self.assertEqual(item["type"], "registry:item", item["name"])
            for f in item["files"]:
                self.assertTrue(f["target"].startswith("~/"), f"{item['name']}: {f['path']}")
        rejected = {"$schema": "x", "name": "x", "homepage": "x", "items": [
            {"name": "Bad Name", "type": "registry:item", "files": [{"path": "nope.css", "type": "registry:file"}]}]}
        import json
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "registry.json"
            bad.write_text(json.dumps(rejected))
            real = af.REGISTRY
            try:
                af.REGISTRY = bad
                found = af.registry_problems()
            finally:
                af.REGISTRY = real
        self.assertTrue(any("lowercase" in f for f in found))
        for item in af.registry()["items"]:
            for dep in item.get("registryDependencies", []):
                self.assertTrue(dep.startswith(f"{af.REGISTRY_REPO}/"), f"{item['name']}: bare {dep!r} would resolve to shadcn/ui")
        self.assertTrue(any("does not exist" in f for f in found))
        self.assertTrue(any("target" in f for f in found))

    def test_skill_lists_every_component(self):
        skill = (af.ROOT / ".claude" / "skills" / "airframe" / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: airframe\n"))
        for comp in af.components():
            if comp["name"] != "Cover":
                self.assertIn(f"| {comp['name']} |", skill, comp["name"])
        self.assertLess(skill.count("\n"), 500, "SKILL.md stays under 500 lines (Agent Skills guidance)")


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
