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

After the latest Windows restart, at 2026-10-05 23:51:14 +08:00, the physical host
free-space measurements were:

| Host volume | Free bytes | Free GiB | Prior workflow-start reference |
|---|---:|---:|---:|
| `C:` | 94,410,817,536 | 87.9269 | 76.00 GiB |
| `E:` | 86,889,463,808 | 80.9221 | 76.60 GiB |

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

Windows restarted again at 2026-10-05 23:39:41 +08:00. The BCD change took
effect: `HypervisorPresent=True` and `HvHost` is running. However, the DISM log
shows that the preceding Virtual Machine Platform enable command failed at
23:39:15 with `0x800706be`; its cleanup also reported `0x800706ba` and
`0x800401fd`. The reboot therefore occurred without deploying HCS.

The component store contains versioned `vmcompute.exe` payloads, but
`C:\Windows\System32\vmcompute.exe`, `hcsdiag.exe`, and the `vmcompute` service
registration are absent. The next minimal action is to rerun only the failed
feature command in an elevated PowerShell after Windows is fully started:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
Restart-Computer
```

Do not restart unless DISM exits successfully and reports that the operation
completed. `bcdedit` does not need to be repeated. If DISM again returns an
RPC/component-servicing error, Microsoft documents `DISM /Online
/Cleanup-Image /RestoreHealth` followed by `sfc /scannow` as the bounded repair
for missing or corrupted system files; rerun the feature command only after
those repairs complete. The actual pipeline should resume only after
Ubuntu-22.04 starts; it should then measure mounts, graphroot, memory, and the
corrected resource plan before any large download.

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
