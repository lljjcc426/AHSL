# AP-R0 candidate families

| Family | Boundary | Serious candidates | Early conclusion |
|---|---|---|---|
| A Data/analytics | hybrid structured-vector execution, adaptive execution, reuse/lineage | A1 hybrid relational-vector current gap; A2 adaptive query stability | new benchmark evidence exists, but bounded executable artifacts did not |
| B Reliable AI/agents | objectively executable workflows, recovery and state | B1 programmatically verified business workflows; B2 live SWE agents | benchmarks improved; current strong baseline remains model/API dependent |
| C SE + AI/program systems | test generation, repository analysis, verified transformation | C1 repository test generation; C2 incremental analysis | executable targets exist; no locally current strong-baseline residual was reproduced |
| D Compiler/runtime | dynamic shapes and compilation cost/correctness | D1 current PyTorch dynamic compilation | local build failed; official 2026 evidence reports the targeted performance gap closed |
| E Scientific/optimization | semantic constraint modeling and objective workloads | E1 CP-Bench; E2 current solver competitions | CP-Bench benchmark runs, but current semantic baseline was unavailable; generic solving is mature |
| F Security/fuzzing verification | fuzz-found vulnerability repair plus semantic verification | F1 AutoPatchBench/ARVO | justified by multiple recent artifacts; exact dual-container baseline was inaccessible |

Family F is included because AutoPatchBench, ARVO, SecCodeBench and 2026
security-repair evaluations converge on a stable, objectively checked security
problem with public artifacts. It is treated separately from generic code repair
because crash reproduction, fuzzing and behavioral differential validation are
part of the task definition. Its infrastructure burden nevertheless prevented a
bounded current residual test.
