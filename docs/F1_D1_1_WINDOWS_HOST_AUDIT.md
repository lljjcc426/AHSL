# F1-D1.1 Windows host audit

Audit time: 2026-08-28 23:26 CST (UTC+08:00)

This audit was read-only. No Windows feature, WSL distribution, Docker data, disk layout, BIOS/UEFI setting, or benchmark artifact was changed.

## Host

| Field | Observed value |
|---|---|
| Windows | Microsoft Windows 11 Home Chinese |
| Version / build | 10.0.26200 / 26200 |
| Architecture | 64-bit |
| CPU | 13th Gen Intel Core i9-13900H |
| Physical / logical processors | 14 / 20 |
| Physical RAM | 33,968,340,992 bytes (31.6 GiB) |
| Administrator shell | No |

## Storage

| Drive | Filesystem | Capacity (GiB) | Free (GiB) |
|---|---:|---:|---:|
| C | NTFS | 486.6 | 60.4 |
| D | NTFS | 495.9 | 100.1 |
| E | NTFS | 440.6 | 268.2 |
| F | NTFS | 458.0 | 230.2 |

The AHSL checkout is on `E:`. Capacity is recorded only; Docker feasibility and the WSL ext4 storage plan have not yet been accepted because WSL2 cannot currently start.

## Virtualization evidence

| Signal | Observed value |
|---|---|
| Virtualization enabled in firmware | True |
| VM Monitor Mode Extensions | True |
| Second Level Address Translation | True |
| DEP available | True |
| Windows hypervisor present | False |
| `vmcompute` service | Not installed (`OpenService FAILED 1060`) |

The hardware prerequisites are present. The missing Windows compute service and absent hypervisor, together with the WSL launch error documented in `F1_D1_1_WSL_AUDIT.md`, support classification **VIRT-B**: hardware virtualization is available, but the required Windows feature stack is not active.

This is not evidence for VIRT-C; no BIOS/UEFI change is indicated.

## Required user action

Run the following once in **PowerShell opened as Administrator**:

```powershell
wsl --install --no-distribution
```

This uses the supported WSL installer to enable/update the required Windows components without installing another Linux distribution. If Windows requests a restart, restart manually; Codex will not reboot the host.

