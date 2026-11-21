"""Transparent always-on-top overlay that paints the ESP boxes."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget

from esp_core.pipeline.esp_pipeline import EspPipeline
from esp_core.models.esp_frame import EspFrame


class OverlayWindow(QWidget):
    def __init__(self, pipeline: EspPipeline, cfg) -> None:
        super().__init__()
        self.pipeline = pipeline
        self.cfg = cfg

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.showFullScreen()

        self.frame: EspFrame | None = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(cfg.tick_ms)

    def _tick(self) -> None:
        self.frame = self.pipeline.next_frame()
        self.update()

    def paintEvent(self, _event) -> None:
        if not self.frame:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for box in self.frame.boxes:
            pen = QPen(QColor(box.color))
            pen.setWidth(2)
            p.setPen(pen)
            p.drawRect(box.x, box.y, box.w, box.h)
            if self.cfg.show_labels:
                p.drawText(box.x + 4, box.y - 4, box.label)