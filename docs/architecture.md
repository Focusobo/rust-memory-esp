# Architecture

```
bootstrap  ->  EntityReader  ->  EspPipeline  ->  OverlayWindow
                    ^                 |
                    |                 +-- PlayerFilter
                    |                 +-- BoneSkeletonProcessor
                    |                 +-- LootFilter
                    |
             RustProcess (pymem, read-only)
```

## Layers
- `esp_app/` — Qt overlay + bootstrap.
- `esp_core/pipeline/` — frame assembly per tick.
- `esp_core/processors/` — per-entity filters / projection helpers.
- `esp_core/services/` — process attach, memory reads, W2S, offsets.
- `esp_core/models/` — dataclasses for entities and render frames.
- `esp_core/utils/` — math, logger, config loader.

## Anti-cheat note
This project reads from `RustClient.exe` with `PROCESS_VM_READ` only. It does not
allocate, write, or inject. Do not run this on official Facepunch servers unless you
accept that bans are permanent and expected.