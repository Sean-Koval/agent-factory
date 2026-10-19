"""config.yaml: everything site-specific, in the bot repo. Secrets are files mounted from your secret manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bot.relay import Routing


@dataclass
class Config:
    bdk_config: str                       # the Symphony BDK's own config (pod, bot username, RSA key path)
    hangar_url: str
    secrets: dict[str, str] = field(default_factory=dict)  # name -> mounted file
    webhook_port: int = 8080
    routing: Routing = field(default_factory=Routing)

    def secret(self, name: str) -> str:
        return Path(self.secrets[name]).read_text().strip()


def from_dict(d: dict[str, Any]) -> Config:
    r = d.get("routing") or {}
    return Config(bdk_config=d["symphony"]["bdk_config"], hangar_url=d["hangar"]["url"],
                  secrets=dict(d.get("secrets") or {}), webhook_port=int(d.get("webhook", {}).get("port", 8080)),
                  routing=Routing(projects=dict(r.get("projects") or {}), default=dict(r.get("default") or {})))


def load(path: Path) -> Config:
    import yaml

    return from_dict(yaml.safe_load(path.read_text()))
