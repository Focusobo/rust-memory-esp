"""Filter players by FOV, team, max distance and visibility."""
from __future__ import annotations

from esp_core.models.player_entity import PlayerEntity


class PlayerFilter:
    def __init__(self, cfg) -> None:
        self.max_distance = cfg.esp.max_distance_m
        self.show_teammates = cfg.esp.show_teammates
        self.min_health = cfg.esp.min_health
        self.only_alive = cfg.esp.only_alive

    def apply(self, players: list[PlayerEntity]) -> list[PlayerEntity]:
        out = []
        for p in players:
            if self.only_alive and p.health <= 0:
                continue
            if p.health < self.min_health:
                continue
            if p.distance_m > self.max_distance:
                continue
            if not self.show_teammates and p.is_teammate:
                continue
            out.append(p)
        return out