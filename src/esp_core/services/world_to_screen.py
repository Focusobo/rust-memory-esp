"""World-to-screen projection for the overlay."""
from __future__ import annotations

from dataclasses import dataclass

from esp_core.utils.math3d import Vec3


@dataclass
class ScreenPoint:
    x: float
    y: float
    on_screen: bool


class WorldToScreen:
    def __init__(self, matrix: list[float], width: int = 1920, height: int = 1080) -> None:
        self.m = matrix
        self.w = width
        self.h = height

    def project(self, world: Vec3) -> ScreenPoint | None:
        m = self.m
        cx = world.x * m[0] + world.y * m[4] + world.z * m[8] + m[12]
        cy = world.x * m[1] + world.y * m[5] + world.z * m[9] + m[13]
        cw = world.x * m[3] + world.y * m[7] + world.z * m[11] + m[15]
        if cw < 0.001:
            return None
        nx, ny = cx / cw, cy / cw
        sx = (self.w / 2) * (nx + 1)
        sy = (self.h / 2) * (1 - ny)
        return ScreenPoint(sx, sy, 0 <= sx <= self.w and 0 <= sy <= self.h)