"""Shared logger configured with colorama + file sink."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from colorama import Fore, init


def setup_logger(level: int = logging.INFO) -> None:
    init(autoreset=True)
    root = logging.getLogger()
    root.setLevel(level)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(f"{Fore.CYAN}[%(name)s]{Fore.RESET} %(message)s"))
    root.addHandler(console)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    fh = RotatingFileHandler(log_dir / "esp.log", maxBytes=2_000_000, backupCount=3)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(fh)