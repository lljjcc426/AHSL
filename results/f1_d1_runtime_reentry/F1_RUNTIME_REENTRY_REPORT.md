# F1-D1 Runtime Re-entry Report

Audit date: 2026-10-04 (Asia/Shanghai)

## 1. Generic runtime status

The Linux boot blocker is cleared. WSL2, Ubuntu 22.04, Docker Engine, Podman,
the compiler/debugger toolchain, Python venv creation, and the Codex CLI binary
are operational. The revised generic readiness command returns **PARTIAL** with
exit code 1 because host-backed free space is 47.2 GiB, below the unchanged
50 GiB floor. All non-storage generic checks pass.

`ahsl_ok` means only that `/home/cc/research/AHSL/.git` exists. `python_ok`
means only that the system interpreter can create and execute a temporary venv.
`codex_cli_ok` means only that `codex --version` succeeds; it does not imply
authentication or model access.

## 2. F1 environment and protocol tests

The dedicated environment is
`/home/cc/.venvs/ahsl-f1-d1-runtime-reentry`, using Python 3.12.15. Only
`pytest`, `pandas`, and their direct runtime dependencies were installed. The
system Python was not replaced and `sudo pip` was not used.

The required command completed successfully:

```text
PYTHONPATH=src /home/cc/.venvs/ahsl-f1-d1-runtime-reentry/bin/python -m pytest -q tests/test_f1_d1_protocol.py
12 passed in 0.60s
```

The full log and JUnit XML are retained. `legacy_full_suite=NOT_RUN`; this is
not a claim that the whole AHSL repository passes.

During log normalization, a failed PowerShell NUL-byte replacement truncated
eight newly created logs. No source, historical result, environment, XML/JSON,
or exit-code artifact was affected. The locally reproducible commands were run
again to restore their logs; the external agent probe was not repeated, and its
replacement log is explicitly marked as a recovery record backed by the
preserved exit code and structured usage JSON. No project file was deleted.

## 3. Single-instance resource feasibility

**STORAGE_BLOCKED.** Docker and rootless Podman data both reside inside the
Ubuntu VHDX on host volume `C:`. Final measured free space was 46.87 GiB; the
VHDX occupied 15.48 GiB. Existing Podman storage used 7.6 GiB physically and
reported 15.62 GB of logical images. No existing image was removed.

Official guidance is approximately 500 GB for 20 sample cases, or 25 GB per
case on average. A bounded single-instance planning estimate is 25 GiB for the
vulnerable/fixed and derived images, 12 GiB for concurrent download/unpack/build
overhead, 8 GiB for fuzzing and differential temporary state, and 1 GiB for
logs: 46 GiB incremental peak. Preserving the 50 GiB floor requires at least
96 GiB free before starting, or 49.1 GiB more than currently available. Because
no Development image manifests were fetched, this is a planning lower bound,
not proof of sufficient peak capacity. A practical arrangement should expose
at least 110 GiB free on the volume backing the container store.

No Lite-wide pull, Development image pull, VHDX move, partition change, user
data cleanup, or global container prune was performed.

## 4. Benchmark container and verifier status

The frozen artifact remains PurpleLlama commit
`4be64c3a24442b51c76175e6ec67722cc3f5fe38`. Its official implementation uses
Podman and builds separate `n132/arvo:<id>-vul` and `-fix` derivatives; the fixed
chain includes the differential-debugging dependencies and a 10-minute QA run.

Podman 3.4.4 can run the already-present generic `hello-world` image, with
cgroup-manager fallback warnings. This is only generic runtime evidence.
`benchmark_container_sanity=NOT_RUN` and `verifier_sanity=NOT_RUN` because the
storage gate failed before any Development instance was selected. Consequently
no Development image tag or digest is claimed.

## 5. Agent and baseline status

The intended envelope was not expanded: one outer trajectory, one candidate,
3600 seconds, `gpt-5.6-luna`, reasoning `none`, plugins disabled, ephemeral,
and vulnerable-checkout-only workspace write access. The installed CLI is
0.160.0 rather than the previously audited 0.149.1.

The required WSL-local access probe used an empty directory and read-only
sandbox. `codex login status` returned `Not logged in`, no API key was present,
and both WebSocket and HTTPS returned 401. The probe produced no model output
or usage record. Therefore `agent_access_ok=BLOCKED` and the baseline
configuration is **blocked before re-freeze**, not silently migrated.

No Development instance was selected. All 25 frozen Development rows were
excluded from this run by the global storage and authentication gates before
outcome-dependent selection was possible. The 87-instance UNTOUCHED pool was
not accessed. Instance 10445 remains `ANALYSIS-EXPOSED`; its existing images
were listed for storage accounting only and were not run.

Baseline trajectory: **NOT_RUN**. V0, V1, V2, V3, and V4 are each `NOT_RUN`.

## 6. Remaining blockers and stop decision

1. Add at least 49.1 GiB of capacity to the volume backing the container store;
   63.1 GiB additional is the recommended minimum to reach 110 GiB free. Do not
   infer that another current drive is sufficient without relocating the VHDX
   or container store through an explicit, reviewed storage plan.
2. Authenticate the WSL-native Codex CLI using the approved existing account
   route, then repeat exactly one read-only access probe. No credentials belong
   in Git or reports.
3. After both gates pass, determine one Development instance using only the
   predeclared infrastructure rule, record its base/derived image digests, and
   run official evaluator controls before the single baseline trajectory.

The task stops at these explicit pre-execution blockers as required. It does
not expand to the Development pool and does not introduce a repair mechanism.

## 7. Later storage-semantics clarification

The 96 GiB and 110 GiB figures above are planning estimates derived from broad
sample guidance, not measured single-instance peaks or protection thresholds.
The underlying 46.87 GiB host measurement and the original resource record are
preserved. A later 10445-specific audit uses an explicit incremental estimate,
uncertainty margin, and the unchanged 50 GiB reserve.
