"""Loot container / dropped item entity."""
from __future__ import annotations

import math
from dataclasses import dataclass

from esp_core.utils.math3d import Vec3


@dataclass
class LootEntity:
    name: str
    position: Vec3
    distance_m: float

    @classmethod
    def from_memory(cls, pm, list_base: int, idx: int, offsets) -> "LootEntity":
        entry = pm.read_longlong(list_base + offsets.off("loot_list.stride") * idx)
        pos = Vec3(
            pm.read_float(entry + offsets.off("loot.pos.x")),
            pm.read_float(entry + offsets.off("loot.pos.y")),
            pm.read_float(entry + offsets.off("loot.pos.z")),
        )
        name_ptr = pm.read_longlong(entry + offsets.off("loot.name_ptr"))
        name = pm.read_string(name_ptr) if name_ptr else "unknown"
        return cls(name=name, position=pos, distance_m=math.hypot(pos.x, pos.y, pos.z))