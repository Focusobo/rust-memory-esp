"""Optional skeleton drawing (bones only, no aim assist)."""
from __future__ import annotations

from esp_core.models.esp_frame import EspBox
from esp_core.models.player_entity import PlayerEntity
from esp_core.services.world_to_screen import WorldToScreen


class BoneSkeletonProcessor:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def build(self, player: PlayerEntity, w2s: WorldToScreen) -> list[EspBox]:
        boxes: list[EspBox] = []
        for joint in player.bones:
            sp = w2s.project(joint)
            if not sp or not sp.on_screen:
                continue
            boxes.append(EspBox(x=sp.x - 2, y=sp.y - 2, w=4, h=4, color="#ffffff", label=""))
        return boxes