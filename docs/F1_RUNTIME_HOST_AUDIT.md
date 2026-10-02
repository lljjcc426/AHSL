# F1 runtime host audit

Audit time: 2026-10-02 22:44 CST (UTC+08:00)

The audit was non-destructive. It did not change Windows features, boot settings, BIOS/UEFI, partitions, WSL distributions, or container data.

## Windows host

| Field | Observed value |
|---|---|
| Edition | Microsoft Windows 11 Home Chinese |
| Version / build | 10.0.26200 / 26200 |
| Architecture | 64-bit x86 |
| CPU | 13th Gen Intel Core i9-13900H |
| Logical CPUs | 20 |
| Physical RAM | 31.6 GiB |
| Administrator shell | No |

## Host storage

| Drive | Filesystem | Capacity (GiB) | Free (GiB) |
|---|---:|---:|---:|
| C | NTFS | 486.6 | 55.6 |
| D | NTFS | 495.9 | 90.7 |
| E | NTFS | 440.6 | 71.1 |
| F | NTFS | 458.0 | 91.7 |

The existing Ubuntu VHDX is on `C:` and currently occupies 14.14 GiB. The host-side capacity governing further VHDX growth is therefore approximately 55.6 GiB, not the virtual capacity reported inside Linux. Storage classification is **STORAGE-C** (`<250 GB usable`).

## WSL and virtualization

| Signal | Observed value |
|---|---|
| WSL package | 2.5.9.0 |
| WSL kernel package | 6.6.87.2-1 |
| Default WSL version | 2 |
| Ubuntu-22.04 | Installed, stopped, WSL2 |
| docker-desktop | Installed, stopped, WSL2 |
| Firmware virtualization | True |
| Second Level Address Translation | True |
| Windows hypervisor present | False |
| `vmcompute` service | Not installed (`OpenService FAILED 1060`) |
| Ubuntu launch | Failed: `HCS_E_SERVICE_NOT_AVAILABLE` |

The hardware prerequisites are present, so this is a Windows component/configuration blocker (category A), not evidence that BIOS virtualization is disabled.

## Required manual action

Open PowerShell as Administrator and run:

```powershell
wsl --install --no-distribution
```

If Windows requests a restart, restart manually. No automatic reboot was attempted.

