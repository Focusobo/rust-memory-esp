"""Offsets loaded from offsets/offsets.json, keyed by build hash."""
from __future__ import annotations

import json
from pathlib import Path


class OffsetTable:
    def __init__(self, data: dict) -> None:
        self._chains: dict[str, list[int]] = data["chains"]
        self._offsets: dict[str, int] = data["offsets"]
        self.build = data.get("build", "unknown")

    @classmethod
    def from_file(cls, path: Path) -> "OffsetTable":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def chain(self, name: str) -> list[int]:
        return self._chains[name]

    def off(self, name: str) -> int:
        return self._offsets[name]