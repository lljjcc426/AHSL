# F1 Linux runtime bootstrap report

## 1. Executive result

**READY for the requested generic Linux runtime.** WSL2, Docker Engine,
compilers, CMake, LLDB, Python venv creation, Codex CLI, and the native Linux
AHSL checkout all passed their direct checks. Storage remains **STORAGE-C**.

No scientific benchmark, security target, fuzzer, repair agent, exploit input,
reference fix, or vulnerability case was inspected or run.

## 2. Windows and WSL

The host is Windows 11 Home Chinese 10.0.26200 on an Intel Core i9-13900H with
20 logical CPUs and 31.6 GiB RAM. WSL 2.5.9.0 now boots Ubuntu 22.04.5 LTS on
kernel `6.6.87.2-microsoft-standard-WSL2` as `x86_64`. The Windows hypervisor
and `vmcompute` service are active.

## 3. Effective resources

WSL exposes 20 logical CPUs, 15.4 GiB RAM, and 4.0 GiB swap. The Ubuntu VHDX
occupies 14.87 GiB on `C:`, whose current free space is 53.2 GiB. The ext4
filesystem's 943 GiB virtual free space is not treated as physically usable
capacity.

## 4. Docker

Ubuntu's native Docker Engine 29.1.3 and containerd are active and enabled.
Docker uses `overlayfs` and cgroup v2. The ordinary-user checks passed:

- `docker version` and `docker info`
- `docker run --rm hello-world`
- `docker run --rm ubuntu:24.04 uname -m` -> `x86_64`

The Ubuntu 24.04 image was fetched through `docker.m.daocloud.io` after a direct
Docker Hub layer transfer stalled, then tagged locally as `ubuntu:24.04`. The
Docker daemon configuration was not changed.

## 5. Native toolchain

- GCC/G++ 11.4.0 and Clang 14.0.0
- CMake 3.22.1 and Ninja 1.10.1
- LLDB 14.0.0
- Git 2.34.1

A trivial C program compiled and ran, LLDB launched that program in batch mode,
and a separate minimal CMake C++ project configured, built, and ran.

## 6. Python and Codex CLI

Python 3.10.12 successfully created and executed a temporary venv. Node
22.23.3 and npm 10.9.9 were installed under `/home/cc/.nvm`; Linux-native
`codex-cli 0.160.0` runs successfully.

The AHSL package metadata declares Python `>=3.11`, while this Ubuntu release's
system Python is 3.10. The project dependency environment was intentionally not
installed and `pytest` was not run: most scientific dependencies are absent,
and installing them would exceed the generic infrastructure-only scope. This
does not affect the generic Python venv check, but it must be addressed before
a later repository test or scientific execution phase.

## 7. AHSL checkout

The native Linux checkout is `/home/cc/research/AHSL`. It is clean, on branch
`project-f1-runtime-bootstrap`, tracking
`origin/project-f1-runtime-bootstrap`, at checkpoint
`8bca3215798288ff4584d5038b528ddb36778f61` before this report update.

## 8. Runtime readiness

`scripts/check_f1_runtime_readiness.py` now checks architecture, WSL2, Docker,
the Ubuntu 24.04 container, direct compilation, CMake, LLDB, Python venv,
Codex CLI, the native AHSL checkout, and host-backed free space. Its final
output is:

```text
architecture_ok=true
wsl2_ok=true
docker_ok=true
container_ok=true
compiler_ok=true
cmake_ok=true
debugger_ok=true
python_ok=true
codex_cli_ok=true
ahsl_ok=true
disk_free_gb=53.2
ram_gb=15.4
cpu_count=20
READY
```

## 9. Environment changes

- Installed Ubuntu packages: `docker.io` and its runtime dependencies; existing
  compiler, CMake, LLDB, Python, and Git packages were retained.
- Added user `cc` to the `docker` group.
- Changed `/etc/apt/sources.list` from the slow Ubuntu endpoints to the USTC
  mirror for the same Jammy repositories.
- Created `/home/cc/.nvm` and updated `/home/cc/.profile` through the nvm
  installer.
- Removed only the empty stale nvm lock directory created by the interrupted
  first Node download. No project file or container data was deleted.

## 10. Remaining constraint

There is no blocker for the generic runtime bootstrap. STORAGE-C and the absent
Python >=3.11 project environment remain explicit constraints for later work;
no scientific execution should be inferred from this infrastructure result.

## 2026-10-04 post-bootstrap re-entry note

The Linux boot/runtime result remains valid. A dedicated Python 3.12 F1
environment now passes the 12 F1 protocol tests. Current generic readiness is
`PARTIAL`, not because WSL or Docker regressed, but because the host-backed free
space is now below the unchanged 50 GiB floor. F1 benchmark readiness is
separately `BLOCKED` by storage and WSL-native Codex authentication. This note
does not rewrite the measurements or conclusion at the original bootstrap time.
