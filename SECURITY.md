# Security policy

`rust-memory-esp` is a **read-only external ESP** for the Rust client. It uses
`OpenProcess(PROCESS_VM_READ)` and `ReadProcessMemory` only. We do **not** ship write
primitives, aim-assist hooks, or any injected DLL.

## Supported versions
| Branch | Supported |
|--------|-----------|
| main   | yes       |
| dev    | best-effort |

## Reporting a vulnerability
If you find a crash-on-attach, an out-of-bounds read that bluescreens, or a way the
overlay leaks the host process handle, open a private security advisory on GitHub.
Do **not** post working POCs that crash other people's hosts.

## Out of scope
- Anti-cheat bypass reports (we don't bypass anything).
- "My account got banned" — that's the nature of using cheats on official servers.
- Requests for kernel-mode components.