"""The copy-me templates in examples/: placeholders only, coherent policy files, and their own tests pass.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
TEMPLATES = [EXAMPLES / "company-overlay", EXAMPLES / "symphony-bot"]
TEXT = {".md", ".py", ".yaml", ".yml", ".toml", ".tf", ".tfvars", ".sh", ".txt", ""}
# The only suite names a company template may carry: where it gets hangar and the suite's docs from.
ALLOWED_SUITE = re.compile(r"(?i)sean-koval(/(hangar|agent-factory|team-harness)(\.git)?|/\*|\.github\.io(/[\w.-]+)?)")


def _files() -> list[Path]:
    return [p for t in TEMPLATES for p in sorted(t.rglob("*"))
            if p.is_file() and p.suffix in TEXT and "__pycache__" not in p.parts]


def _yaml(path: Path) -> list[dict]:
    import yaml

    return [d for d in yaml.safe_load_all(path.read_text()) if d is not None]


class PlaceholdersTest(unittest.TestCase):
    def test_no_personal_or_company_values(self) -> None:
        bad = []
        for p in _files():
            text = p.read_text()
            rel = p.relative_to(ROOT)
            if "PROJECT_ID" in text:
                bad.append(f"{rel}: PROJECT_ID (Sean's install's sed placeholder)")
            if re.search(r"(?i)\bacme\b", text):
                bad.append(f"{rel}: 'acme': use example-org or <company>")
            for m in re.finditer(r"(?i)sean[\w.-]*(/[\w.*-]+)?", text):
                if not ALLOWED_SUITE.fullmatch(m.group(0)):
                    bad.append(f"{rel}: {m.group(0)}")
            for m in re.finditer(r"https?://([\w.-]+)", text):
                host = m.group(1).lower()
                if not (host.endswith(("example.com", "example.net", "github.com", "github.io", "atlassian.net"))
                        or host in ("localhost",)):
                    bad.append(f"{rel}: URL host {host}")
        self.assertEqual(bad, [])


@unittest.skipIf(importlib.util.find_spec("yaml") is None, "PyYAML not installed")
class PolicyTest(unittest.TestCase):
    POLICY = EXAMPLES / "company-overlay" / "agent-factory-deploy" / "policy"
    SCHEMAS = {"hangar.repo-policy/v1", "hangar.changeset-profile/v1", "hangar.credential/v1"}

    def test_every_yaml_parses(self) -> None:
        for p in _files():
            if p.suffix in (".yaml", ".yml"):
                with self.subTest(p=str(p.relative_to(ROOT))):
                    _yaml(p)

    def test_policy_documents(self) -> None:
        docs = {p: _yaml(p) for p in sorted(self.POLICY.rglob("*.yaml"))}
        repos = {d["repo"] for ds in docs.values() for d in ds if d["schema"] == "hangar.repo-policy/v1"}
        creds = {d["name"] for ds in docs.values() for d in ds if d["schema"] == "hangar.credential/v1"}
        for p, ds in docs.items():
            for d in ds:
                with self.subTest(p=str(p.relative_to(ROOT)), name=d.get("name") or d.get("repo")):
                    self.assertIn(d.get("schema"), self.SCHEMAS)
                    if d["schema"] == "hangar.credential/v1":
                        self.assertEqual(d["source"], f"file:/var/run/hangar-secrets/{d['name']}")
                    if d["schema"] == "hangar.changeset-profile/v1":
                        self.check_profile(d, repos)
        mounted = (EXAMPLES / "company-overlay" / "agent-factory-deploy" / "components" / "credentials" /
                   "kustomization.yaml").read_text()
        self.assertEqual(creds, set(re.findall(r"secretKey: ([\w-]+)", mounted)))

    def check_profile(self, d: dict, repos: set[str]) -> None:
        roles = d["repos"]
        dep = d["deploy"]
        self.assertTrue(set(d["land_order"]) <= set(roles))
        self.assertNotIn(dep["role"], d["land_order"])
        self.assertEqual(roles[dep["role"]].get("agent"), "read", "the agent never edits the deploy repo")
        self.assertEqual(set(dep["after"]), set(d["land_order"]))
        for role, r in roles.items():
            self.assertIn(r["repo"], repos, f"{d['name']}.{role}: no repo policy for {r['repo']}")


class TemplateTestsTest(unittest.TestCase):
    def test_symphony_bot_tests(self) -> None:
        bot = EXAMPLES / "symphony-bot"
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=bot,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-3000:])

    @unittest.skipIf(importlib.util.find_spec("pydantic") is None, "pydantic not installed")
    def test_bump_plugin_tests(self) -> None:
        plugin = EXAMPLES / "company-overlay" / "agent-factory-bots" / "plugins" / "hangar-example-bump"
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=plugin,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-3000:])


if __name__ == "__main__":
    unittest.main()
