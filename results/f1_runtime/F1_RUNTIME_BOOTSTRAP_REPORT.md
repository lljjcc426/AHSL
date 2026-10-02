# F1 Linux runtime bootstrap report

## 1. Executive result

**BLOCKED.** The requested generic Linux runtime cannot currently boot. Hardware virtualization is available, but the Windows virtualization compute component is absent. No scientific benchmark, security target, fuzzer, repair agent, or reference fix was accessed or run in this task.

## 2. Windows host

Windows 11 Home Chinese, version 10.0.26200, build 26200, on a 64-bit Intel Core i9-13900H host.

## 3. WSL status

WSL 2.5.9.0 is installed. `Ubuntu-22.04` and `docker-desktop` are registered as WSL2 distributions but stopped. Starting Ubuntu fails with `Wsl/Service/CreateInstance/CreateVm/HCS/HCS_E_SERVICE_NOT_AVAILABLE`. The `vmcompute` service is absent and Windows reports no active hypervisor.

## 4. Ubuntu

Ubuntu-22.04 is installed but could not be booted. Its current architecture and release files could not be re-verified in this session.

## 5. CPU/RAM

The host exposes 20 logical CPUs and 31.6 GiB RAM. Effective WSL CPU, RAM, and swap remain unmeasured because the VM cannot start.

## 6. Storage

The Ubuntu VHDX resides on `C:`, occupies 14.14 GiB, and can currently grow only into approximately 55.6 GiB of host free space. This is STORAGE-C. No VHDX move or resize was attempted.

## 7. Docker

Docker Engine was not installed or tested because WSL2 cannot start. Docker hello-world and Ubuntu container status are BLOCKED. No container data was deleted.

## 8. Compiler

Generic GCC/Clang and CMake sanity are BLOCKED pending Ubuntu startup.

## 9. Debugger

LLDB version and trivial-program launch are BLOCKED pending Ubuntu startup.

## 10. Python

Python and temporary virtual-environment sanity are BLOCKED pending Ubuntu startup.

## 11. Codex CLI

Codex CLI inside WSL was not inspected because Ubuntu cannot start. No credentials were accessed or copied.

## 12. AHSL clone

The Windows checkout is on branch `project-f1-runtime-bootstrap`, created exactly from `b6adeb481335006550987fd4ecdc49a69f7743b8`. The required native Linux clone cannot be verified until WSL starts.

## 13. Runtime readiness

The generic readiness script is `scripts/check_f1_runtime_readiness.py`. Current status is **BLOCKED** because `wsl2_ok=false`; Docker, compiler, debugger, Python, and native-clone checks have not been represented as passes.

## 14. Remaining blockers

The required Windows virtualization component is not active. The current shell is not elevated, so this task cannot enable it. This is a Windows component/configuration blocker, not a BIOS or unsupported-hardware classification.

## 15. Exact next action

Open PowerShell as Administrator and run:

```powershell
wsl --install --no-distribution
```

If prompted, restart Windows manually. Then resume this task; the first command will be:

```powershell
wsl -d Ubuntu-22.04 -- uname -a
```
