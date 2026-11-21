"""Read the entity list, local player, and loot containers out of Rust memory."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from esp_core.services.process_attach import RustProcess, read_ptr_chain
from esp_core.services.offset_table import OffsetTable
from esp_core.models.player_entity import PlayerEntity
from esp_core.models.loot_entity import LootEntity
from esp_core.utils.math3d import Vec3


@dataclass
class _LocalPlayer:
    position: Vec3
    team_id: int


class EntityReader:
    def __init__(self, proc: RustProcess, offsets: OffsetTable) -> None:
        self.proc = proc
        self.offsets = offsets
        self.pm = proc.pm
        self._tick = 0
        self._local: _LocalPlayer | None = None

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def local_team(self) -> int:
        return self._local.team_id if self._local else -1

    def view_matrix(self) -> list[float]:
        addr = read_ptr_chain(self.pm, self.proc.base, self.offsets.chain("camera"))
        return [self.pm.read_float(addr + i * 4) for i in range(16)]

    def _read_local(self) -> None:
        try:
            addr = read_ptr_chain(self.pm, self.proc.base, self.offsets.chain("local_player"))
            pos = Vec3(
                self.pm.read_float(addr + self.offsets.off("local.position.x")),
                self.pm.read_float(addr + self.offsets.off("local.position.y")),
                self.pm.read_float(addr + self.offsets.off("local.position.z")),
            )
            team = self.pm.read_int(addr + self.offsets.off("local.team_id"))
            self._local = _LocalPlayer(position=pos, team_id=team)
        except Exception as exc:  # noqa: BLE001
            logging.getLogger("esp.reader").debug("local read failed: %s", exc)

    def read_players(self) -> list[PlayerEntity]:
        self._tick += 1
        self._read_local()
        base_list = read_ptr_chain(self.pm, self.proc.base, self.offsets.chain("entity_list"))
        count = self.pm.read_int(base_list + self.offsets.off("entity_list.count"))
        out: list[PlayerEntity] = []
        for i in range(min(count, 512)):
            try:
                out.append(PlayerEntity.from_memory(self.pm, base_list, i, self.offsets))
            except Exception:  # noqa: BLE001
                continue
        return out

    def read_loot(self) -> list[LootEntity]:
        base_list = read_ptr_chain(self.pm, self.proc.base, self.offsets.chain("loot_list"))
        count = self.pm.read_int(base_list + self.offsets.off("loot_list.count"))
        return [
            LootEntity.from_memory(self.pm, base_list, i, self.offsets)
            for i in range(min(count, 256))
        ]