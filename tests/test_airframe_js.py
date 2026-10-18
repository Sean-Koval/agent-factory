"""Tests for airframe/js/airframe.js, the optional helpers module. Run: python3 -m unittest discover -s tests

The string helpers run under `node --test` (tests/airframe_js.test.mjs) when node is installed, as it is in CI; the
rest checks the module's contract from Python: no dependencies, no build step, no color literals, the published copy.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import airframe as af  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = af.HELPERS
TEST = ROOT / "tests" / "airframe_js.test.mjs"


class HelpersTests(unittest.TestCase):
    def test_module_is_dependency_free_and_published(self):
        text = SRC.read_text()
        self.assertNotRegex(text, r"^\s*import\s", "airframe.js must not import anything")
        self.assertNotIn("require(", text)
        self.assertNotIn("customElements", text, "no Web Components (Sean's decision)")
        self.assertEqual(af.color_literals(text), [], "no color literals in the helpers")
        self.assertEqual((af.THEME / "airframe.js").read_text(), text, "theme/airframe.js is the published copy; run build")
        for name in ("status", "icon", "meta", "btn", "avatar", "obj", "tag", "toast", "confirm", "inhibited", "flush"):
            self.assertRegex(text, rf"export function {name}\(", name)
        self.assertIn("export const drawer", text)

    def test_helpers_speak_the_contracts(self):
        text = SRC.read_text()
        for role in ("running", "queued", "approval", "failed", "denied", "off"):
            self.assertIn(f"{role}:", text)
        for cls in ("af-status__mark", "af-meta__key", "af-btn--text", "af-avatar--", "af-obj__trust", "af-toast__msg",
                    "af-dialog__foot", "af-drawer", "af-scrim", "af-drawer-open--bottom"):
            self.assertIn(cls, text, cls)
        # the three decision buttons of a confirm run refuse then accept; inspect, when present, is first
        self.assertRegex(text, re.compile(r"inspect \? btn\(.*?\)\s*:\s*\"\"\}\$\{btn\(cancel.*?\}\$\{btn\(ok", re.S))

    @unittest.skipUnless(shutil.which("node"), "node is not installed; the string helpers are tested in CI")
    def test_string_helpers_under_node(self):
        run = subprocess.run(["node", "--test", str(TEST)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertRegex(run.stdout, r"# fail 0")


if __name__ == "__main__":
    unittest.main()
