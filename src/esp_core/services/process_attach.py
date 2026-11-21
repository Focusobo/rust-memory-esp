"""Open a read-only handle to the Rust client."""
from __future__ import annotations

import ctypes
import logging
from dataclasses import dataclass

import pymem
from pymem.process import module_from_name

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

log = logging.getLogger("esp.attach")


@dataclass
class RustProcess:
    pm: pymem.Pymem
    base: int
    size: int


def attach_to_rust(exe_name: str = "RustClient.exe") -> RustProcess | None:
    try:
        pm = pymem.Pymem(exe_name)
    except pymem.exception.ProcessNotFound:
        log.warning("%s not found", exe_name)
        return None
    except Exception as exc:  # noqa: BLE001
        log.exception("attach failed: %s", exc)
        return None

    mod = module_from_name(pm.process_handle, exe_name)
    if mod is None:
        log.error("could not resolve base module for %s", exe_name)
        return None

    log.info("attached to pid=%s base=0x%x", pm.process_id, mod.lpBaseOfDll)
    return RustProcess(pm=pm, base=mod.lpBaseOfDll, size=mod.SizeOfImage)


def read_ptr_chain(pm: pymem.Pymem, base: int, offsets: list[int]) -> int:
    addr = base
    for i, off in enumerate(offsets):
        addr = pm.read_longlong(addr + off)
        if addr == 0:
            raise ValueError(f"null in pointer chain at index {i}")
    return addr