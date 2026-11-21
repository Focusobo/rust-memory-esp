# Contributing to rust-memory-esp

Thanks for wanting to help out with **rust-memory-esp** — a Python memory-reading ESP + overlay
toolkit aimed at the Rust (Facepunch) client on Windows.

## Ground rules
- Everything here targets the **official Steam client of Rust** for educational / private-server
  research. Do not submit code that targets anti-cheat protected services you don't own.
- Do not open PRs that add kernel drivers, HWID spoofers, or anything that bypasses kernel-mode
  anti-cheat. Userspace read-only ESP is in scope; kernel stuff is not.
- Keep offsets in `offsets/offsets.json` up to date. Every offset PR must include the game build
  hash in the commit body.

## Dev setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m rust_esp --config config/default.yaml
```

## Code style
- Python 3.11+, type hints everywhere, `ruff` + `black` clean.
- No `print()` in `src/esp_core/` — use the `logging` module via `utils/logger.py`.
- Every new feature gets a stub test under `tests/`.

## Pull request flow
1. Fork, branch as `feature/<short-name>` or `fix/<short-name>`.
2. Run `pytest -q` locally.
3. Attach a screenshot of the overlay (blur out UIDs) if it's a visual change.