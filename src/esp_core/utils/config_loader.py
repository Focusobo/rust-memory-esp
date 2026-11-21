"""YAML config loader with dataclass wrappers."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class EspCfg:
    max_distance_m: float = 400.0
    show_teammates: bool = False
    min_health: int = 1
    only_alive: bool = True
    show_labels: bool = True


@dataclass
class LootCfg:
    enabled: bool = True
    max_distance_m: float = 150.0
    whitelist: list[str] = field(default_factory=list)


@dataclass
class AppConfig:
    target_process: str = "RustClient.exe"
    tick_ms: int = 16
    esp: EspCfg = field(default_factory=EspCfg)
    loot: LootCfg = field(default_factory=LootCfg)


def load_config(path: Path) -> AppConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig(
        target_process=raw.get("target_process", "RustClient.exe"),
        tick_ms=raw.get("tick_ms", 16),
        esp=EspCfg(**raw.get("esp", {})),
        loot=LootCfg(**raw.get("loot", {})),
    )