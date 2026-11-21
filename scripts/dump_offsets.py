"""Utility: print the current RustClient module layout for offset hunting."""
from __future__ import annotations

import sys

from esp_core.services.process_attach import attach_to_rust


def main() -> int:
    proc = attach_to_rust()
    if proc is None:
        print("RustClient.exe not running", file=sys.stderr)
        return 1
    print(f"pid      : {proc.pm.process_id}")
    print(f"base     : 0x{proc.base:08X}")
    print(f"size     : 0x{proc.size:X}")
    print(f"build    : see offsets/offsets.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())