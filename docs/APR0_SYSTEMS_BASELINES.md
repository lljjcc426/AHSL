# AP-R0 systems baselines

| Candidate | Current fair baseline | Same-system control | Why it was not executed or selected |
|---|---|---|---|
| hybrid vector-relational | current systems in Hybrid-ANNS plus RVBench engines | each engine's own optimized filtered/hybrid route | datasets and heterogeneous setup exceeded pre-gate; dense ACORN/SIEVE/DIGRA/RangePQ collision |
| executable agents | current public agent on AutomationBench/SWE-bench Live | agent with/without recovery/verification component | current model/API output unavailable; historical leaderboard values are insufficient |
| test generation | current repository-level code model/agent | same generator with official test/evaluation loop | current inference unavailable |
| dynamic compilation | PyTorch 2.13 recommended automatic dynamic shapes/user annotations vs eager/static | yes, planned within PyTorch | compile did not reach execution; official current parity evidence closes the hypothesized performance gap |
| constraint synthesis | current LLM plus CP-Bench evaluator and CPMpy/solver | same model with official prompting/inference-time modes | benchmark ran; current model output did not |
| security repair | current repair agent plus AutoPatchBench verifier | same agent before/after fuzz/differential filtering | dual-container and current model route unavailable |

Old academic baselines, disabled optimizations and unrelated cross-system speed
comparisons were not used. A missing baseline cell remains `NA`; it is not
filled using paper-reported historical numbers.
