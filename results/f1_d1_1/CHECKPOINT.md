# F1-D1.1 checkpoint: Windows feature activation required

Status at 2026-08-28 23:26 CST:

- branch started exactly from `b6adeb481335006550987fd4ecdc49a69f7743b8`;
- Windows host audit completed without mutation;
- hardware virtualization, VM monitor extensions, and SLAT are available;
- Windows reports no active hypervisor and has no `vmcompute` service;
- `Ubuntu-22.04` is installed as WSL2 but cannot start, returning `HCS_E_SERVICE_NOT_AVAILABLE`;
- classification is VIRT-B;
- AutoPatchBench was not executed or changed;
- the 25-case Development split, 87-case untouched pool, and case 10445 status were not changed;
- no benchmark image, Docker image, package, or large artifact was downloaded;
- no repair intervention was implemented.

## REBOOT REQUIRED

In PowerShell opened as Administrator, run:

```powershell
wsl --install --no-distribution
```

If prompted, reboot Windows manually. After reboot, resume with:

```powershell
wsl -d Ubuntu-22.04 -- uname -a
```

Do not create a new Ubuntu distribution unless the existing `Ubuntu-22.04` is later shown unusable by direct evidence.

