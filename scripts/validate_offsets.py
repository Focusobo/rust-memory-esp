"""Sanity-check that every offset in offsets.json resolves to readable memory."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from esp_core.services.process_attach import attach_to_rust, read_ptr_chain


def main() -> int:
    proc = attach_to_rust()
    if proc is None:
        print("RustClient.exe not running", file=sys.stderr)
        return 1

    data = json.loads(Path("offsets/offsets.json").read_text(encoding="utf-8"))
    bad = 0
    for name, chain in data["chains"].items():
        try:
            addr = read_ptr_chain(proc.pm, proc.base, chain)
            print(f"OK  {name:<15} -> 0x{addr:016X}")
        except Exception as exc:  # noqa: BLE001
            bad += 1
            print(f"BAD {name:<15} : {exc}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())