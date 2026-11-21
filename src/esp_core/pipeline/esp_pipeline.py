"""Pipeline that turns memory reads into renderable ESP frames."""
from __future__ import annotations

import logging
from collections import deque

from esp_core.services.entity_reader import EntityReader
from esp_core.services.world_to_screen import WorldToScreen
from esp_core.processors.player_filter import PlayerFilter
from esp_core.processors.bone_skeleton import BoneSkeletonProcessor
from esp_core.processors.loot_filter import LootFilter
from esp_core.models.esp_frame import EspFrame, EspBox


class EspPipeline:
    def __init__(self, reader: EntityReader, cfg) -> None:
        self.log = logging.getLogger("esp.pipeline")
        self.reader = reader
        self.w2s = WorldToScreen(reader.view_matrix())
        self.player_filter = PlayerFilter(cfg)
        self.skeleton = BoneSkeletonProcessor()
        self.loot = LootFilter(cfg)
        self._history: deque[EspFrame] = deque(maxlen=8)

    def next_frame(self) -> EspFrame:
        players = self.reader.read_players()
        loot = self.reader.read_loot()
        boxes: list[EspBox] = []

        for pl in self.player_filter.apply(players):
            screen = self.w2s.project(pl.position)
            if screen is None or not screen.on_screen:
                continue
            boxes.append(
                EspBox.from_world(
                    screen=screen,
                    head=pl.head_offset_m,
                    color="#ff3355" if pl.team_id != self.reader.local_team else "#33ff88",
                    label=f"{pl.name} [{pl.distance_m:.0f}m] HP:{pl.health}",
                )
            )
            if self.skeleton.enabled:
                boxes.extend(self.skeleton.build(pl, self.w2s))

        for item in self.loot.apply(loot):
            screen = self.w2s.project(item.position)
            if screen and screen.on_screen:
                boxes.append(EspBox.from_world(screen=screen, color="#ffd633", label=item.name))

        frame = EspFrame(boxes=boxes, tick=self.reader.tick)
        self._history.append(frame)
        return frame