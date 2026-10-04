# F1 runtime resource audit

Audit time: 2026-10-03 00:17 CST (UTC+08:00)

## Host resources

- Logical CPUs: 20
- RAM: 31.6 GiB
- Ubuntu VHDX location: `C:\Users\cc\AppData\Local\wsl\{ea43aa54-76b9-435e-bd5d-dc990288f070}\ext4.vhdx`
- Ubuntu VHDX current file size: 14.87 GiB
- Governing host drive free space: 53.2 GiB
- Storage class: **STORAGE-C**

## WSL resources

| Resource | Observed value |
|---|---:|
| Logical CPUs | 20 |
| RAM | 15.4 GiB |
| Swap | 4.0 GiB |
| Root filesystem | ext4, 1007 GiB virtual capacity |
| Root virtual free space | 943 GiB |

The ext4 capacity is sparse virtual capacity and must not be used as the
storage classification input. The runtime readiness script therefore measures
`/mnt/c` while running under WSL2 and reports 53.2 GiB free.

No `.wslconfig` resource tuning was added. The current allocation is sufficient
for generic compilation, debugger, Python, and container checks. STORAGE-C does
not justify claiming capacity for a full scientific run or a large retained
container/dataset cache.

## 2026-10-04 F1-D1 re-entry measurement

The Ubuntu VHDX grew to 15.48 GiB and host `C:` free space fell to 46.87 GiB.
Docker uses `/var/lib/docker`; rootless Podman uses
`/home/cc/.local/share/containers/storage`. Both paths are inside the same VHDX
and therefore consume `C:`. The frozen 50 GiB protection floor was not lowered.
Single-instance benchmark preparation is `STORAGE_BLOCKED`; no benchmark image
download or cleanup was started.
