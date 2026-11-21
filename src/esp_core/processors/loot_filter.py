"""Filter and label loot containers for the ESP."""
from __future__ import annotations

from esp_core.models.loot_entity import LootEntity


class LootFilter:
    def __init__(self, cfg) -> None:
        self.enabled = cfg.loot.enabled
        self.max_distance = cfg.loot.max_distance_m
        self.whitelist = set(cfg.loot.whitelist or [])

    def apply(self, loot: list[LootEntity]) -> list[LootEntity]:
        if not self.enabled:
            return []
        out = []
        for item in loot:
            if item.distance_m > self.max_distance:
                continue
            if self.whitelist and item.name not in self.whitelist:
                continue
            out.append(item)
        return out