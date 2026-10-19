import asyncio
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import hangar_example_bump as bump  # noqa: E402

DIGEST = "sha256:" + "ab" * 32


class Ctx:
    def __init__(self, environment: str = "dev") -> None:
        self.environment = environment
        self.calls: list[tuple[list[str], str]] = []
        self.notes: list[str] = []

    async def exec(self, cmd: list[str], cwd: str) -> None:
        self.calls.append((cmd, cwd))

    def audit(self, note: str) -> None:
        self.notes.append(note)


class BumpTest(unittest.TestCase):
    def test_registers_one_deliverer(self) -> None:
        added = []
        bump.plugin.register(SimpleNamespace(add_deliverer=added.append), bump.Settings())
        self.assertEqual([d.kind for d in added], ["example-kustomize-bump"])
        self.assertEqual(bump.plugin.api, "hangar.plugin/v1")

    def test_sets_the_overlay_image_by_digest(self) -> None:
        ctx = Ctx("dev")
        d = bump.KustomizeBump(bump.Settings())
        asyncio.run(d.apply(ctx, SimpleNamespace(image="registry.example.com/agent-factory/hangar", digest=DIGEST)))
        self.assertEqual(ctx.calls, [(["kustomize", "edit", "set", "image",
                                       f"ghcr.io/sean-koval/hangar=registry.example.com/agent-factory/hangar@{DIGEST}"],
                                      "overlays/dev")])
        self.assertEqual(len(ctx.notes), 1)

    def test_refuses_a_tag_or_an_escape(self) -> None:
        d = bump.KustomizeBump(bump.Settings())
        with self.assertRaises(ValueError):
            asyncio.run(d.apply(Ctx(), SimpleNamespace(image="x", digest="latest")))
        escape = bump.KustomizeBump(bump.Settings(overlay_dir="../{environment}"))
        with self.assertRaises(ValueError):
            asyncio.run(escape.apply(Ctx(), SimpleNamespace(image="x", digest=DIGEST)))


if __name__ == "__main__":
    unittest.main()
