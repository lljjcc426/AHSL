# F1-D1.1 WSL audit

Audit time: 2026-08-28 23:26 CST (UTC+08:00)

## Installed state

| Field | Observed value |
|---|---|
| WSL package version | 2.5.9.0 |
| Linux kernel package | 6.6.87.2-1 |
| WSLg | 1.0.66 |
| Default WSL version | 2 |
| Default distribution | docker-desktop |
| Ubuntu distribution | Ubuntu-22.04, stopped, WSL version 2 |
| docker-desktop distribution | stopped, WSL version 2 |
| `WslService` | Running |
| `vmcompute` | Service absent |
| Windows `docker` command | Not found |
| Windows `podman` command | Not found |
| `%UserProfile%\.wslconfig` | Absent |

## Launch probe

The following non-destructive probe was attempted:

```powershell
wsl -d Ubuntu-22.04 -- uname -a
```

It failed before the distribution started:

```text
Wsl/Service/CreateInstance/CreateVm/HCS/HCS_E_SERVICE_NOT_AVAILABLE
```

This prevents Ubuntu filesystem, systemd, Docker Engine, toolchain, architecture, and benchmark sanity checks. No package or image download was attempted.

## Classification and checkpoint

Current virtualization classification: **VIRT-B**.

This is an infrastructure checkpoint, not a final I-A/I-B/I-C/I-D result. WSL has not been shown unsuitable; one administrator-level feature activation and a possible user-controlled reboot remain before that judgment is possible.

After the required Windows action and any requested reboot, the first resumption probe is:

```powershell
wsl -d Ubuntu-22.04 -- uname -a
```

If it succeeds, continue with the native WSL ext4 location and storage audit before Docker installation or image pulls. If the same HCS failure remains, re-audit the enabled Windows features from an elevated shell and decide whether WSL is still proportionate to pursue.

