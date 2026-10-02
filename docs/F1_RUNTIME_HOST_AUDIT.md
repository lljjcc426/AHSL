# F1 runtime host audit

Audit time: 2026-10-03 00:17 CST (UTC+08:00)

## Windows host

| Field | Observed value |
|---|---|
| Edition | Microsoft Windows 11 Home Chinese |
| Version / build | 10.0.26200 / 26200 |
| Architecture | 64-bit x86 |
| CPU | 13th Gen Intel Core i9-13900H |
| Logical CPUs | 20 |
| Physical RAM | 31.6 GiB |

## Host storage

| Drive | Filesystem | Capacity (GiB) | Free (GiB) |
|---|---:|---:|---:|
| C | NTFS | 486.6 | 53.2 |
| D | NTFS | 495.9 | 90.7 |
| E | NTFS | 440.6 | 71.1 |
| F | NTFS | 458.0 | 91.7 |

The Ubuntu VHDX is on `C:` and occupies 14.87 GiB. Its practical growth is
therefore governed by 53.2 GiB of host free space, not the 943 GiB virtual free
space reported by ext4. Storage classification remains **STORAGE-C** (`<250 GB
usable`).

## WSL and virtualization

| Signal | Observed value |
|---|---|
| WSL package | 2.5.9.0 |
| WSL kernel | 6.6.87.2-microsoft-standard-WSL2 |
| Default WSL version | 2 |
| Ubuntu-22.04 | Running, WSL2, x86_64 |
| Ubuntu release | Ubuntu 22.04.5 LTS |
| Windows hypervisor present | True |
| `vmcompute` service | Running |

The earlier `HCS_E_SERVICE_NOT_AVAILABLE` blocker was cleared after the user
enabled the required Windows components and restarted Windows. No BIOS/UEFI or
partition change was made by this task.

## Linux runtime services

Docker Engine and containerd run as native Ubuntu systemd services and are
enabled for later WSL sessions. User `cc` belongs to the `docker` group, so the
Docker CLI works without an elevated shell.
