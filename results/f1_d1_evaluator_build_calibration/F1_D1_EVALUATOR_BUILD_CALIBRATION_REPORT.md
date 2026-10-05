# F1-D1 Actual Dependency Build and Evaluator Calibration

Run date: 2026-10-05 (Asia/Shanghai)

## Outcome

The two prerequisite implementation defects are fixed and the affected tests
pass. Actual dependency execution did not start because Ubuntu-22.04 cannot
create its WSL2 VM: `HCS_E_SERVICE_NOT_AVAILABLE`. This is a concrete Windows
runtime blocker, not a dependency-build failure and not a storage-blocked
conclusion.

No source archive, image, build, package, or evaluator process was started.
No Development instance was selected, no baseline was run, no model request
was sent, and the UNTOUCHED pool was not accessed.

## Implemented fixes

1. The generated `lldb-python.sh` now appends `PYTHONPATH` and
   `LD_LIBRARY_PATH` safely when either variable is unset, empty, or already
   populated. A real Bash regression test executes all three states under
   `set -u`.
2. Resource output now separates workflow-start cumulative occupancy from
   remaining incremental occupancy based on persisted successful checkpoints.
   First-target, second-target, split-volume, same-volume, and package-resume
   behavior are covered by focused tests. The reserve floor remains 50 GiB.
3. The build now starts the staged Python 3.7.17 and imports `ctypes`,
   `sqlite3`, and `ssl` before LLVM configuration. It no longer invokes the
   broad LLVM install target. The selected install targets cover `lldb`,
   `liblldb`, Python bindings, `lldb-argdumper`, `lldb-server`, and Clang
   resource headers.
4. Cache, package-content, ELF, and dynamic-link checks now include
   `lldb-server`; package testing still requires the real LLDB Python API and
   a debug launch of `/bin/true`.

The narrowed target choice follows the LLVM 13.0.1 build definitions, where
LLDB tools and the shared API library have component install targets, the
Python package has its own install target, and the Python package depends on
`liblldb` and `lldb-argdumper`.

Focused test result: **15 passed in 0.20 s**, exit code 0. The saved run used
Windows Python 3.11.5 because WSL could not start. The required rerun with the
existing F1 Python 3.12 environment is `NOT_RUN`, not inferred from this result.

## Current resource evidence

At 2026-10-05 15:44:20 +08:00, the physical host free-space measurements were:

| Host volume | Free bytes | Free GiB | Prior workflow-start reference |
|---|---:|---:|---:|
| `C:` | 99,803,717,632 | 92.9495 | 76.00 GiB |
| `E:` | 87,109,492,736 | 81.1270 | 76.60 GiB |

Both physical volumes exceed the prior cumulative planning references after
the user's cleanup. Those numbers alone are not a current execution PASS.
Because WSL could not start, the current `/mnt/e` backing relation, Podman
graphroot, retained checkpoint sizes, and WSL available memory could not be
measured. The corrected incremental plan therefore remains `UNKNOWN` until
those facts are read from the running Linux environment.

## Runtime blocker

The direct Ubuntu-22.04 launch returned exit code 1 with:

`Wsl/Service/CreateInstance/CreateVm/HCS/HCS_E_SERVICE_NOT_AVAILABLE`

Observed Windows state:

- firmware virtualization, VM monitor extensions, and SLAT: enabled;
- `HypervisorPresent`: false;
- `WslService`: running;
- `HvHost`: stopped and cannot be started without elevation;
- `vmcompute`: not installed or not registered;
- `wsl --status`: reports that the current configuration does not support
  WSL2 and directs enabling Virtual Machine Platform.

Because `wsl --install --no-distribution` was already run, the next minimal
action is a Windows restart to activate the requested feature change. If the
same error remains after restart, elevated PowerShell is required to inspect
the `VirtualMachinePlatform` feature and BCD `hypervisorlaunchtype`; ordinary
permissions cannot read those states here. The actual pipeline should resume
only after Ubuntu-22.04 starts; it should then measure mounts, graphroot,
memory, and the corrected resource plan before any large download.

## Stage status

| Stage | Status | Evidence |
|---|---|---|
| prerequisite code fixes | PASS | 15 focused tests |
| WSL path and mount check | BLOCKED | WSL VM creation failed |
| `driver-sync` / `driver-check` | NOT_RUN | Linux runtime unavailable |
| `prepare` | NOT_RUN | no download or image pull started |
| build 20.04 / 16.04 | NOT_RUN | no compiler process started |
| package / package test | NOT_RUN | no `.deb` produced |
| official derived images | NOT_RUN | dependency packages absent |
| evaluator 10445 | NOT_RUN | preceding stages not complete |

No cleanup was performed. No file, directory, image, container, cache, or
historical result was deleted or overwritten.
