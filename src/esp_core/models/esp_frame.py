"""Immutable render frame + box primitive."""
from __future__ import annotations

from dataclasses import dataclass, field

from esp_core.services.world_to_screen import ScreenPoint


@dataclass(frozen=True)
class EspBox:
    x: float
    y: float
    w: float
    h: float
    color: str
    label: str

    @classmethod
    def from_world(cls, screen: ScreenPoint, head: float, color: str, label: str) -> "EspBox":
        h = max(12.0, abs(head) * 4.0)
        w = h * 0.45
        return cls(x=screen.x - w / 2, y=screen.y - h, w=w, h=h, color=color, label=label)


@dataclass(frozen=True)
class EspFrame:
    boxes: list[EspBox] = field(default_factory=list)
    tick: int = 0