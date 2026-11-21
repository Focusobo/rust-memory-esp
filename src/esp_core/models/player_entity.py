"""Player entity decoded from the entity list."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from esp_core.utils.math3d import Vec3


@dataclass
class PlayerEntity:
    name: str
    position: Vec3
    head_offset_m: float
    health: int
    team_id: int
    distance_m: float
    is_teammate: bool = False
    bones: list[Vec3] = field(default_factory=list)

    @classmethod
    def from_memory(cls, pm, list_base: int, idx: int, offsets) -> "PlayerEntity":
        entry = pm.read_longlong(list_base + offsets.off("entity_list.stride") * idx)
        pos = Vec3(
            pm.read_float(entry + offsets.off("player.pos.x")),
            pm.read_float(entry + offsets.off("player.pos.y")),
            pm.read_float(entry + offsets.off("player.pos.z")),
        )
        head = pm.read_float(entry + offsets.off("player.head_height"))
        name_ptr = pm.read_longlong(entry + offsets.off("player.name_ptr"))
        name = pm.read_string(name_ptr) if name_ptr else "?"
        return cls(
            name=name,
            position=pos,
            head_offset_m=head,
            health=pm.read_int(entry + offsets.off("player.health")),
            team_id=pm.read_int(entry + offsets.off("player.team_id")),
            distance_m=math.hypot(pos.x, pos.y, pos.z),
        )