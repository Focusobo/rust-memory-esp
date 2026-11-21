"""Smoke tests that don't require RustClient.exe to be running."""
from __future__ import annotations

from esp_core.pipeline.esp_pipeline import EspPipeline
from esp_core.utils.config_loader import AppConfig
from esp_core.utils.math3d import Vec3
from esp_core.models.player_entity import PlayerEntity


class _StubReader:
    tick = 1
    local_team = 1

    def view_matrix(self) -> list[float]:
        return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    def read_players(self) -> list[PlayerEntity]:
        return [
            PlayerEntity("Alice", Vec3(0, 0, 10), 1.8, 100, 2, 10.0),
            PlayerEntity("Bob",   Vec3(0, 0, 20), 1.8, 100, 1, 20.0),
        ]

    def read_loot(self):
        return []


def test_pipeline_produces_frame() -> None:
    cfg = AppConfig()
    pipe = EspPipeline(reader=_StubReader(), cfg=cfg)
    frame = pipe.next_frame()
    assert frame.tick == 1
    assert isinstance(frame.boxes, list)