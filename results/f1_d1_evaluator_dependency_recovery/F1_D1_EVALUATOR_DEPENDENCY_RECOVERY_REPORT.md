# F1-D1 Evaluator Dependency Recovery Report

Audit date: 2026-10-05 (Asia/Shanghai)

## Outcome

The dependency-recovery implementation is ready, but execution is storage
blocked. No source archive, Python/LLVM/LLDB build, package, derived image, or
evaluator container was started. The current result is therefore **recovery
implementation prepared, resources not authorized/available**, not an
unresolved source-build design gap and not a completed evaluator calibration.

No Development instance was selected, no baseline was run, and the UNTOUCHED
pool was not accessed.

The previously passing F1 protocol suite and the legacy full repository suite
were not rerun: `f1_protocol_tests=NOT_RERUN` and
`legacy_full_suite=NOT_RUN`.

## Upstream and source decision

`meta-llama/PurpleLlama` issue 123 remains open. Its only follow-up repeats the
S3 `AccessDenied` condition and provides no official package or replacement
retrieval path. The prior 403 object URL was not requested again; Codex login
and ordinary AWS credentials were not treated as bucket authorization.

The bounded fallback starts from `safety-research/PurpleLlama` commit
`8a98628dc7941972c96ffac5e3f8fed839ad336a`. All three build files were read
before adapting them. Only the MIT-licensed dependency build sequence was used;
the frozen benchmark stays at `meta-llama/PurpleLlama` commit
`4be64c3a24442b51c76175e6ec67722cc3f5fe38`. No unknown prebuilt package is
used and source-built packages are not represented as byte-identical to the
unavailable official binaries.

## Delivered implementation

`scripts/f1_d1_evaluator_dependency_recovery.py` exposes these separate stages:

| Stage | Purpose | Current status |
|---|---|---|
| `plan` | Per-volume, per-phase resource decision | PASS as an audit; overall plan BLOCKED |
| `driver-check` | Static closure plus real Python import | BLOCKED at missing `pkg_resources` |
| `driver-sync` | Venv-only install from the dedicated closure file | NOT_RUN: storage gate |
| `prepare` | Pinned source archives, base images, runtime library | NOT_RUN: storage gate |
| `build --target` | Explicit target, CPU jobs, and memory | NOT_RUN |
| `package` | Build both real `.deb` packages | NOT_RUN |
| `test` | Metadata, ELF, dynamic links, import/API/debug function | NOT_RUN |

Work, cache, output, logs, container store, and backing host volumes are all
explicit. Large-I/O stages require an explicit flag plus a passing stage
budget. The script never invokes host `sudo`/`apt`, never uses a shared fixed
temporary directory, refuses incomplete caches and existing output overwrite,
and records each command and stage exit code. Optional cleanup is limited to a
successfully completed run directory created by the script. It was not invoked
in this run.

Both required package names are produced from non-empty installed trees:
`differential-debugging-deps-16.04.deb` and
`differential-debugging-deps-20.04.deb`. Package tests require amd64 metadata,
Python 3.7.17, LLDB 13, resolved dynamic libraries, `import lldb`, valid LLDB
Python objects, and a real `/bin/true` debug launch. None of these runtime tests
is claimed as passed before packages exist.

The static implementation tests passed: **9 passed in 0.30 s**. The earlier
9-pass run's shell wrapper lost its `PIPESTATUS` after pytest and returned 1;
that raw log is retained. The authoritative final run has pytest exit code 0
and a JUnit record with 9 tests, 0 failures, and 0 errors.

## Driver dependency closure

The actual frozen AutoPatch import closure contains 11 external imports. Nine
map directly to the frozen CybersecurityBenchmarks requirements, `botocore` is
provided transitively by `boto3`, and `requests` is imported directly but is
not declared there. The dedicated requirement file adds `requests==2.33.0`,
the version pinned elsewhere in the same frozen repository commit. This is an
explicit local recovery addition, not an upstream AutoPatch declaration.

The external checkout was sparse and omitted `benchmark/llms`. That directory
was materialized from existing objects at the same frozen commit; no source
content or commit changed and no network download was required. Static closure
resolution now has zero unresolved local modules. The real driver import still
fails first at `pkg_resources`, so driver dependencies are not marked ready.

## Phase resource budget

Existing occupancy is reflected in host free space, not added again: the
Ubuntu VHDX is 15.60 GiB, the Podman graph root uses 7.51 GiB physically, and
Podman reports 15.62 GB of logical image content. The VHDX and Podman store are
both physically backed by `C:`; task artifacts are configured on `E:`.

| Phase | Incremental/retained basis | `E:` required start-free | `C:` required start-free |
|---|---|---:|---:|
| Driver dependencies | 0.5 cache + 0.1 logs; 0.75 WSL venv | 51.70 GiB | 54.75 GiB |
| Source preparation | 3.0 cache + 0.1 logs; 1.0 WSL/Podman | 54.20 GiB | 55.00 GiB |
| First build | 14 work + 4 cache + 0.25 logs; 3 WSL/Podman | 73.35 GiB | 57.00 GiB |
| Second build | 14 work + 7 retained cache + 0.5 logs; 5 WSL/Podman | 76.60 GiB | 59.00 GiB |
| Packaging | 5 work + 7 cache + 2 output + 0.5 logs; 5 WSL/Podman | 70.10 GiB | 59.00 GiB |
| Package test | 7 cache + 2 output + 0.75 logs; 7 WSL/Podman | 61.35 GiB | 61.00 GiB |
| Official derivatives | retained artifacts; 14 WSL/Podman | 61.35 GiB | 68.00 GiB |
| 10445 evaluator | retained artifacts; 22 WSL/Podman | 61.60 GiB | 76.00 GiB |

Each required value already includes the unchanged 50 GiB reserve and the
separate role uncertainty margins (4 GiB active work, 1 GiB cache, 0.5 GiB
output, 0.1 GiB logs, 4 GiB WSL/Podman). The 14 GiB active build allowance uses
the fork's roughly 10 GiB statement only as a starting point, with extraction
and install staging added; it is not presented as a measured peak.

The final plan snapshot measured 64.06 GiB free on `E:` and 46.28 GiB on `C:`.
The complete source-build plus isolated evaluator route is short by 12.54 GiB
on `E:` and 29.72 GiB on `C:`. The old 27.17 GiB figure covered a narrower plan
and is not reused as this route's release condition. For driver dependencies
alone, `C:` is short by 8.47 GiB.

Preferred minimal change under the current layout: make at least 76.60 GiB
free on `E:` and 76.00 GiB free on `C:`, then rerun `plan`. This means adding or
freeing at least 12.54 GiB and 29.72 GiB respectively at the recorded snapshot.
Any cleanup, movement of user data, VHDX/container-store migration, or
partition change requires separate user selection and authorization; none was
performed.

## Authentication and execution boundary

WSL user `cc` is logged in through ChatGPT with Codex CLI 0.160.0. Exactly one
actual read-only probe was sent to frozen model `gpt-5.6-luna` with reasoning
`none`, one trajectory, and a 60-second limit. It returned `ACCESS_OK` with
11,559 input tokens (3,840 cached), 6 output tokens, and 0 reasoning tokens.
Three earlier launcher/PATH failures sent no model request and are retained as
separate logs. No model, billing route, or budget was changed and no credential
was recorded.

Because storage blocks even the driver installation and source preparation,
10445 engineering calibration remains NOT_RUN. It remains ANALYSIS-EXPOSED and
outside scientific success rates. No package-level check, compile, or generic
container result was substituted for the official differential evaluator.

## Records and file changes

Machine-readable records are under `machine/`; raw outputs are under `logs/`.
No file, image, cache, or user data was deleted. The only external checkout
change was materializing the tracked `CybersecurityBenchmarks/benchmark/llms`
directory through sparse-checkout at the unchanged frozen commit.
