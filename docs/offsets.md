# Updating offsets after a Rust patch

1. Launch Rust, join any test server.
2. Run `python scripts/dump_offsets.py` — grab the new module base.
3. Use ReClass or Cheat Engine to re-locate the four chains in `offsets/offsets.json`:
   `local_player`, `camera`, `entity_list`, `loot_list`.
4. Update the `"build"` field to the current Facepunch build hash.
5. Run `python scripts/validate_offsets.py` — every chain must print `OK`.
6. Open a PR titled `offsets: bump to <build>`.