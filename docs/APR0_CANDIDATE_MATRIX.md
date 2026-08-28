# AP-R0 candidate matrix

Scores use axes A--R in the prompt and are diagnostic only. `B=0` for every
candidate because no executable current material residual passed the gate.

| ID | Direction | Score vector A--R | /90 | Fatal gates | Verdict |
|---|---|---|---:|---|---|
| A1 | hybrid structured-vector execution | 5,0,5,4,4,3,2,5,4,1,2,2,2,1,5,4,5,5 | 59 | G5,G10 | killed |
| B1 | verified business/tool workflows | 5,0,5,4,2,3,2,4,3,4,2,3,2,2,5,4,4,3 | 58 | G5,G10 | killed |
| C1 | repository-level test generation | 5,0,5,4,2,3,2,4,3,4,2,3,2,2,5,4,5,3 | 59 | G5 | killed |
| D1 | current dynamic-shape compilation | 5,0,5,5,5,4,1,5,4,1,3,3,4,2,5,4,5,5 | 66 | G5,G6,G10 | killed |
| E1 | semantic constraint-model synthesis | 4,0,5,3,2,3,3,3,3,5,3,4,5,4,4,4,5,3 | 63 | G5,G6 | killed |
| F1 | fuzz-found vulnerability repair/verification | 5,0,5,5,3,4,3,4,4,5,2,2,2,1,5,5,5,4 | 64 | G5,G11 | killed, not HOLD |

## Serious-candidate records

### A1

Problem: realistic relational predicates and updates can destabilize vector
search tradeoffs. Current system/artifact: Hybrid-ANNS current commit and the
systems it orchestrates. Benchmark: Hybrid-ANNS primary, RVBench secondary.
Executable command: per-system scripts in the repository after external data
setup. Measured residual: `NA`. Mechanism candidates: filter selectivity,
candidate expansion and update/index coupling. Strongest prior art:
ACORN/SIEVE/DIGRA/RangePQ. Why still open: mixed workloads continue to evolve,
but no current residual was reproduced. Possible intervention: cannot be chosen
before G5. First-paper/community: system/algorithm, SIGMOD/PVLDB/ICDE.

### B1

Problem: executable tool workflows fail semantically or recover inefficiently.
Current system/benchmark: AutomationBench/current agents; SWE-bench Live second
route. Executable command: official harness plus a frozen current agent.
Measured residual: `NA`. Mechanism: semantic specification, state or recovery.
Prior art: AgentRx, verifier/retry loops, live agent benchmarks. Open gap and
intervention: not attributable without current traces. Paper community:
ICSE/FSE or task-specific data/AI systems.

### C1

Problem: generated repository tests execute but may not validate intended
behavior. Current artifacts: SAGA/TestGenEval/Vero. Primary/secondary routes:
TestGenEval and real repository evaluation. Current baseline command requires
model inference. Residual: `NA`. Mechanism: incomplete specifications and test
oracle weakness. Prior art is dense in generation, feedback and execution.
Paper community: ISSTA/ICSE/FSE.

### D1

Problem: dynamic shapes may cause recompilation or slow kernels. Current system:
PyTorch 2.13; TorchBench and vLLM routes. The exact pre-gate command is preserved
in `experiments/ap_r0/run_pre_gates.py`. Measured result: two build failures, no
performance ratio. Mechanism of local failures: text decoding and missing MSVC,
not dynamic-shape algorithms. Strongest collision: PyTorch's 2026 parity and
ShapesSpec work. Paper community: PLDI/ASPLOS/MLSys if a distinct residual existed.

### E1

Problem: feasible generated constraint models can misrepresent natural-language
intent. Current artifact: CP-Bench `92ba7dc`; benchmark ground truths and CPMpy
run. Secondary route: MiniZinc/XCSP, though it does not independently validate
language intent. Current baseline generation was not run; residual `NA`.
Mechanism: semantic ambiguity/incomplete specification. Collision: self-
verification, repeated sampling and solver feedback. Community: CP/AAAI/IJCAI/KR.

### F1

Problem: crash-stopping patches often fail fuzzing or semantic preservation.
Current artifact/benchmark: AutoPatchBench; ARVO secondary. Published historical
gap is large, but no current agent was executed. Mechanism: localization,
root-cause search and incomplete behavioral specification. Strong prior art:
AutoPatchBench's fuzz/differential verifier and current security repair systems.
Community: ISSTA/ICSE/FSE/security. The dual-container E4 burden prevents G11
here and does not justify AP-R0-D.
