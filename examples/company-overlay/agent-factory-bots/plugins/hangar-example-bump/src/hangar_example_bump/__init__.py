"""A deliverer plugin (hangar.plugin/v1): after a change set's roles merge and its image exists, point the deploy
repo's overlay at that image by digest. It edits only the deploy checkout hangar gives it, only through `ctx.exec`;
hangar commits, pushes the branch and opens the deploy PR under the deploy repo's own policy.

It runs inside hangar and uses hangar's deliverer types (`hangar.ext.deliverers`, docs/changesets.md):
`apply(ctx, ready)` gets the `Ready` of the profile's `ready` step. With `image-ready` that is
`ready.detail == {"image": "<registry path>:<tag>", "digest": "sha256:..."}`, and `ctx.exec` runs one shell command
line in the checkout and returns hangar's `ExecResult`.
"""

from __future__ import annotations

import re
import shlex
from typing import Any

from hangar.ext.deliverers import DeliverCtx, DeliverError, Ready
from pydantic import BaseModel, Field

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class Settings(BaseModel):
    """HANGAR_PLUGINS.deliverers.hangar-example-bump; a bad value refuses to start hangar."""

    overlay_dir: str = Field("overlays/{environment}", description="the overlay to edit, per environment")
    image_name: str = Field("ghcr.io/sean-koval/hangar", description="the image name the overlay's base uses")


class KustomizeBump:
    """Deliverer `example-kustomize-bump`: `kustomize edit set image NAME=IMAGE@DIGEST` in the overlay."""

    kind = "example-kustomize-bump"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()

    async def ready(self, ctx: DeliverCtx) -> Ready | None:
        return Ready(note="no ready check: pair it with image-ready")  # used as `ready:`, it is ready at once

    async def apply(self, ctx: DeliverCtx, ready: Ready) -> None:
        if ctx.exec is None:
            raise DeliverError(f"{self.kind}: apply needs the deploy repo's checkout")
        ref, digest = str(ready.detail.get("image") or ""), str(ready.detail.get("digest") or "")
        if not ref or not _DIGEST.match(digest):
            raise DeliverError(f"{self.kind}: needs an image-ready step before it (an image and a sha256 digest), "
                               f"got {ready.detail!r}")
        image = ref.rsplit(":", 1)[0] if ":" in ref.rsplit("/", 1)[-1] else ref  # name@digest, not name:tag@digest
        overlay = self.settings.overlay_dir.format(environment=ctx.environment or "")
        if not overlay or overlay.startswith("/") or ".." in overlay.split("/"):
            raise DeliverError(f"{self.kind}: overlay_dir must stay inside the deploy checkout: {overlay!r}")
        target = f"{self.settings.image_name}={image}@{digest}"
        res = await ctx.exec(f"cd {shlex.quote(overlay)} && kustomize edit set image {shlex.quote(target)}")
        if res.exit_code != 0:
            tail = ((res.stdout or "") + (res.stderr or ""))[-600:].strip()
            raise DeliverError(f"{self.kind}: kustomize exited {res.exit_code} in {overlay}: {tail}")
        ctx.audit("deliver.bump", overlay=overlay, image=image, digest=digest)
        ctx.note(f"{overlay}: {self.settings.image_name} -> {image}@{digest[:19]}")


class _Plugin:
    name = "hangar-example-bump"
    api = "hangar.plugin/v1"
    Settings = Settings

    def register(self, host: Any, settings: Settings) -> None:
        host.add_deliverer(KustomizeBump(settings))


plugin = _Plugin()
