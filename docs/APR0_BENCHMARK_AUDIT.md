# AP-R0 benchmark audit

The machine-readable ledger is `results/ap_r0/raw/benchmark_metadata.csv`.

| Candidate | Primary route | Second route | Objective metric | Gate |
|---|---|---|---|---|
| A1 hybrid execution | Hybrid-ANNS/PVLDB current evaluation | RVBench | recall-latency-throughput under relational filters | inaccessible in bounded setup |
| B1 verifiable workflows | AutomationBench | SWE-bench Live or Spider 2.0 | executable task success and cost | current model baseline absent |
| C1 test generation | TestGenEval | SAGA/Vero | tests passing, fault detection, coverage | current model baseline absent |
| D1 dynamic compilation | TorchBench | vLLM workloads | compile success, end-to-end and steady latency | current local build failed; current official parity evidence negative |
| E1 constraint synthesis | CP-Bench | MiniZinc/XCSP | independent semantic correctness, not feasibility alone | primary ground truths usable; current model residual unmeasured |
| F1 security repair | AutoPatchBench | ARVO | build, crash, fuzz and differential validity | container/model route inaccessible |

Hybrid-ANNS, CP-Bench, TestGenEval, SWE-bench and AutoPatchBench are materially
better than toy or synthetic-only routes. Benchmark quality alone is not the
selection gate: only CP-Bench was partly executable here, and running its known
correct models does not expose current model error.
