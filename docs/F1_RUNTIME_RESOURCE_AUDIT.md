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

## 2026-10-04 minimal-unblock storage correction

Benchmark feasibility is now evaluated as
`free - estimated_incremental_peak - uncertainty_margin >= reserve` on each
host volume that actually backs the operation. An unknown instance budget is
`UNKNOWN`, not `PASS`. The approved reserve remains 50 GiB.

For the existing 10445 Podman route, `C:` is the only relevant host volume.
The final snapshot had 46.83 GiB free. The instance-specific planning budget
is 18 GiB incremental peak (9 GiB derived build/intermediate layers, 8 GiB
fuzzing and differential temporary state, 1 GiB logs) plus a separately stated
6 GiB uncertainty margin. The resulting planning requirement is 74 GiB free,
a 27.17 GiB shortfall. This estimate is not a measured build peak.

The earlier 96 GiB minimum-start and 110 GiB recommended-start figures are
planning estimates based on broad sample guidance. They are neither measured
10445 peaks nor changes to the 50 GiB reserve. Their original measurements and
records remain unchanged.
