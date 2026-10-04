# F1-D1 Minimal Unblock and Evaluator Sanity Report

Audit date: 2026-10-04 (Asia/Shanghai)

## Outcome

The storage gate now uses the required operation-aware formula and its two
specified boundary tests pass. The existing F1 environment and prior 12-test
protocol evidence were reused; the environment and protocol suite were not
rebuilt or rerun.

This run stops before evaluator execution. Host storage, WSL authentication,
and evaluator prerequisites do not pass, so no Development baseline was
selected or started.

## Storage decision

The governing volume is `C:` because both the Ubuntu VHDX and rootless Podman
store reside there. The final snapshot shows 46.83 GiB free. Drives D:, E:, and
F: do not enter the decision unless a VHDX or container-store migration is
separately authorized.

For the 10445 reuse route, the planning inputs are:

| Input | GiB | Basis |
|---|---:|---|
| Current host free space | 46.83 | final measurement on C: |
| Derived images and build intermediates | 9 | existing base pair reused; new official derivatives still required |
| Fuzz/differential temporary state | 8 | bounded single-instance planning allowance |
| Logs and retained outputs | 1 | bounded single-instance planning allowance |
| Incremental peak | 18 | sum of the three operation components |
| Uncertainty margin | 6 | separate estimate uncertainty allowance |
| Approved reserve | 50 | unchanged project protection line |

The result is `46.83 - 18 - 6 = 22.83 GiB`, below the 50 GiB reserve.
`benchmark_storage_feasible=BLOCKED`. Starting this plan requires 74 GiB free,
so the minimum current shortfall is 27.17 GiB. This is a targeted planning
estimate, not a measured evaluator peak.

The earlier 96/110 GiB figures are broad planning estimates, not measurements.
An explicit clarification was appended without changing the original resource
records.

## 10445 engineering reuse audit

10445 remains `ANALYSIS-EXPOSED` and is excluded from scientific success
rates. Its vulnerable and fixed base images are present in Podman:

| Image | Digest | Logical size |
|---|---|---:|
| `docker.io/n132/arvo:10445-vul` | `sha256:2d4e8a62c1d800758120fc4540751c29b2aa81c0018a2f766df5fc938dc17af2` | 3.57 GB |
| `docker.io/n132/arvo:10445-fix` | `sha256:f16f1cfedd19f264184b5394790aec44907ca520902fb02131e65c9d4a2ed2dc` | 4.20 GB |

Podman reports their full RootFS storage as shared with two dangling images.
The dangling images have exactly the same 25/31 RootFS layers as the base
pair and add no derived layer, so they are not accepted as the official
`localhost/autopatch:10445-vul/fix` derivatives.

The frozen PurpleLlama commit is
`4be64c3a24442b51c76175e6ec67722cc3f5fe38`. Its official path uses Podman,
builds those two local derivatives, and requires both differential-debugging
`.deb` files. Neither package is local; direct anonymous metadata requests to
the official S3 paths returned HTTP 403. The current F1 environment also lacks
`boto3`, `botocore`, and `async-lru`. No package or image download was started.

Therefore `benchmark_container_sanity=NOT_RUN` and
`verifier_sanity=NOT_RUN`. Ordinary compilation or a generic container check
was not substituted for the official chain.

## Authentication and baseline

Under WSL user `cc`, Codex CLI 0.160.0 reports `Not logged in`. No model request
was sent. Target-model access is `NOT_RUN`, remote support for model/reasoning
parameters is `UNKNOWN`, and `agent_ready=BLOCKED`. The frozen target remains
`gpt-5.6-luna`, reasoning `none`; no model or billing route was changed.

Because storage, agent access, and evaluator calibration did not all pass, no
Development instance was selected. The baseline and V0-V4 are all `NOT_RUN`.
The UNTOUCHED pool was not accessed.

## Required user actions

1. Free at least 27.17 GiB more on host volume C: for the stated 10445 planning
   envelope, or explicitly authorize a reviewed VHDX/container-store migration.
   No user file, image, partition, or VHDX was changed in this run.
2. In the Ubuntu-22.04 WSL session as user `cc`, complete the official
   `codex login` flow with the approved existing account, then report completion.
   The next run will issue exactly one read-only target-model probe.
3. After storage passes, resolve the official dependency retrieval and build
   the two derived images before attempting isolated evaluator controls.

Raw logs are retained unchanged under `logs/`. The machine summary is
`machine/minimal_unblock_status.json`. No file was deleted.
