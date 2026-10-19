"""A deliverer plugin (hangar.plugin/v1): after a change set's roles merge and its image exists, point the deploy
repo's overlay at that image by digest. It edits only the checkout hangar gives it, only through `ctx.exec`, and
hangar pushes the branch and opens the deploy PR under the deploy repo's own policy.

The plugin surface (`register`, `PluginHost.add_deliverer`, `DeliverCtx`, `Ready`) is hangar's `hangar.ext`; this
module names only what it uses, so it imports nothing from hangar.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class Settings(BaseModel):
    """HANGAR_PLUGINS.deliverers.hangar-example-bump; a bad value refuses to start hangar."""

    overlay_dir: str = Field("overlays/{environment}", description="the overlay to edit, per environment")
    image_name: str = Field("ghcr.io/sean-koval/hangar", description="the image name the overlay's base uses")


class KustomizeBump:
    """Deliverer `example-kustomize-bump`: `kustomize edit set image NAME=IMAGE@DIGEST` in the overlay."""

    kind = "example-kustomize-bump"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def ready(self, ctx: Any) -> Any | None:
        return None  # readiness is the profile's `deploy.ready` (image-ready); this deliverer only applies

    async def apply(self, ctx: Any, ready: Any) -> None:
        image, digest = str(ready.image), str(ready.digest)
        if not _DIGEST.match(digest):
            raise ValueError(f"refusing to deploy {image}: '{digest}' is not a sha256 digest")
        overlay = self.settings.overlay_dir.format(environment=ctx.environment)
        if overlay.startswith("/") or ".." in overlay.split("/"):
            raise ValueError(f"overlay_dir must stay inside the deploy checkout: {overlay}")
        await ctx.exec(["kustomize", "edit", "set", "image", f"{self.settings.image_name}={image}@{digest}"],
                       cwd=overlay)
        ctx.audit(f"{overlay}: {self.settings.image_name} -> {image}@{digest}")


class _Plugin:
    name = "hangar-example-bump"
    api = "hangar.plugin/v1"
    Settings = Settings

    def register(self, host: Any, settings: Settings) -> None:
        host.add_deliverer(KustomizeBump(settings))


plugin = _Plugin()
