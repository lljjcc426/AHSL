# F1-D1 benchmark audit

## AutoPatchBench

The official artifact is the `meta-llama/PurpleLlama` repository at commit `4be64c3a24442b51c76175e6ec67722cc3f5fe38` (2026-08-17). Its checked-in `autopatch_lite.json` contains 113 IDs; the repository-level README currently says 120, so the executable dataset is treated as authoritative for this freeze.

Official evaluation builds separate vulnerable and fixed ARVO containers. Generation uses the vulnerable container, build, and original crash. Evaluation adds extended fuzzing and LLDB-based white-box differential state comparison against the fixed container. Lite contains single-hunk ground-truth cases and cannot represent the harder 23-case route described in the original release.

Official current storage guidance is roughly 500GB for the 20-case sample and 2TB for Lite. The current host has about 268GB free on the workspace drive, no Docker/Podman executable, and WSL2 reports unavailable virtualization. Therefore no case can honestly pass infrastructure sanity here.

## SEC-Bench route

SEC-Bench supports vulnerability patching plus PoC generation with Dockerized instances and SWE-agent/OpenHands/Aider/smolagents. Its current setup requires Python 3.12+, Docker, and over 200GB. Its patch-verification semantics are not identical to AutoPatchBench's LLDB differential state comparison, so it is an independent security-repair family, not a drop-in replication comparator. It is audited but not executed in F1-D1.
