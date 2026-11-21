"""Entry point / bootstrap for the rust-memory-esp overlay."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from esp_app.overlay_window import OverlayWindow
from esp_core.services.process_attach import attach_to_rust
from esp_core.services.entity_reader import EntityReader
from esp_core.services.offset_table import OffsetTable
from esp_core.pipeline.esp_pipeline import EspPipeline
from esp_core.utils.logger import setup_logger
from esp_core.utils.config_loader import load_config


def main(argv: list[str] | None = None) -> int:
    setup_logger(level=logging.INFO)
    log = logging.getLogger("esp.bootstrap")

    cfg = load_config(Path("config/default.yaml"))
    offsets = OffsetTable.from_file(Path("offsets/offsets.json"))

    log.info("attaching to %s", cfg.target_process)
    proc = attach_to_rust(cfg.target_process)
    if proc is None:
        log.error("RustClient.exe not running, aborting")
        return 2

    reader = EntityReader(proc, offsets)
    pipeline = EspPipeline(reader=reader, cfg=cfg)

    app = QApplication(argv or sys.argv)
    win = OverlayWindow(pipeline=pipeline, cfg=cfg)
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())