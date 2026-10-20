"""The deliverer against hangar's own types: run with hangar installed (it runs inside hangar's image).

    python -m unittest discover -s tests          # from plugins/hangar-example-bump, hangar importable
"""

import asyncio
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

try:
    from hangar.ext.deliverers import DeliverCtx, DeliverError, Merged, Ready
    from hangar.models import ChangeSet, ExecResult
except ImportError as e:  # pragma: no cover - a checkout without hangar
    raise unittest.SkipTest(f"hangar with change sets is not installed: {e}") from None

import hangar_example_bump as bump  # noqa: E402

DIGEST = "sha256:" + "ab" * 32
IMAGE = "registry.example.com/agent-factory/hangar"
KUSTOMIZATION = """apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources: []
images:
  - name: ghcr.io/sean-koval/hangar
    newName: registry.example.com/agent-factory/hangar
    digest: sha256:BOTS_IMAGE_DIGEST
"""


def ctx(checkout: str | None, exec_=None, environment: str = "dev") -> DeliverCtx:
    cs = ChangeSet(profile="agent-factory", profile_digest="sha256:" + "0" * 64, ticket="jira:SVC-1",
                   parent_job="job-1", primary="code")
    notes: list[str] = []
    c = DeliverCtx(changeset=cs, role="deploy", merged={"code": Merged("example-org/agent-factory-bots", 3, "f" * 40)},
                   environment=environment, spec={"kind": "example-kustomize-bump"}, checkout=checkout, exec=exec_,
                   note=notes.append)
    c.notes = notes  # type: ignore[attr-defined]
    return c


def shell_in(checkout: str):
    """hangar's ctx.exec: one command line, run in the checkout, an ExecResult back."""
    calls: list[str] = []

    async def run(cmd: str) -> ExecResult:
        calls.append(cmd)
        p = subprocess.run(["bash", "-c", cmd], cwd=checkout, capture_output=True, text=True)
        return ExecResult(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr)

    run.calls = calls  # type: ignore[attr-defined]
    return run


READY = Ready(detail={"image": f"{IMAGE}:{'f' * 40}", "digest": DIGEST})


class BumpTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        (Path(self.dir) / "overlays" / "dev").mkdir(parents=True)
        (Path(self.dir) / "overlays" / "dev" / "kustomization.yaml").write_text(KUSTOMIZATION)

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)

    def test_registers_through_hangars_plugin_host(self) -> None:
        from types import SimpleNamespace

        from hangar.ext import deliverers as ext
        from hangar.pluginhost import Host, Loaded

        host = Host(SimpleNamespace(jobs=None, store=None, broker=None, settings=None))
        host._current = Loaded("hangar-example-bump", "0.1.0", builtin=False)  # what load() sets while it registers
        bump.plugin.register(host, bump.Settings())
        self.assertIsInstance(host.deliverers["example-kustomize-bump"], ext.Deliverer)
        self.assertIs(ext.DELIVERERS["example-kustomize-bump"], host.deliverers["example-kustomize-bump"])
        self.assertEqual(bump.plugin.api, ext.API)

    def test_ready_is_immediate(self) -> None:
        self.assertIsInstance(asyncio.run(bump.KustomizeBump().ready(ctx(None))), Ready)

    def test_sets_the_overlay_image_by_digest(self) -> None:
        run = shell_in(self.dir)
        c = ctx(self.dir, run)
        if shutil.which("kustomize") is None:  # still check the one command line hangar would run
            async def fake(cmd: str) -> ExecResult:
                run.calls.append(cmd)
                return ExecResult(exit_code=0, stdout="")
            c.exec = fake
        asyncio.run(bump.KustomizeBump().apply(c, READY))
        self.assertEqual(run.calls, [f"cd overlays/dev && kustomize edit set image "
                                     f"ghcr.io/sean-koval/hangar={IMAGE}@{DIGEST}"])
        if shutil.which("kustomize"):
            text = (Path(self.dir) / "overlays/dev/kustomization.yaml").read_text()
            self.assertIn(DIGEST, text)
            self.assertNotIn("BOTS_IMAGE_DIGEST", text)
        self.assertEqual(len(c.notes), 1)

    def test_a_failed_command_fails_the_step(self) -> None:
        async def failing(cmd: str) -> ExecResult:
            return ExecResult(exit_code=1, stdout="", stderr="no kustomization here")

        with self.assertRaisesRegex(DeliverError, "exited 1"):
            asyncio.run(bump.KustomizeBump().apply(ctx(self.dir, failing), READY))

    def test_refuses_a_tag_an_escape_or_no_checkout(self) -> None:
        d = bump.KustomizeBump()
        with self.assertRaises(DeliverError):
            asyncio.run(d.apply(ctx(self.dir, shell_in(self.dir)), Ready(detail={"image": IMAGE, "digest": "latest"})))
        with self.assertRaises(DeliverError):
            asyncio.run(bump.KustomizeBump(bump.Settings(overlay_dir="../{environment}"))
                        .apply(ctx(self.dir, shell_in(self.dir)), READY))
        with self.assertRaises(DeliverError):
            asyncio.run(d.apply(ctx(None), READY))


if __name__ == "__main__":
    unittest.main()
