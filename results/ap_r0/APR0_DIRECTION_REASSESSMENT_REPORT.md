# AP-R0 Applied Direction Reassessment

Search/execution date: 2026-08-27--28. Frozen base:
`fe9d56c830332c395f69fe86e2f4e1f29496e9c7`.

## 1. Executive decision

**AP-R0-C — NO-GO: STRUCTURED/APPLIED SEARCH SPACE STILL WEAK.** No
candidate reproduced a material current residual against a fair current strong
baseline. The phase therefore selects no parent direction, creates no APR1
proposal and implements no new method/model.

## 2. Why AP1.0 changes selection methodology

AP1.0 showed that a well-supported historical systems concern can disappear in
a current same-engine run. Its recursive incremental matrix was exact, faster
than scratch in every cell and below the frozen memory threshold. The permanent
rule is now: literature bottleneck does not equal current actionable residual.
Artifact + benchmark + current baseline execution precedes method development.

## 3. Search boundary

The audit covered at most six application-oriented families and did not expand
to generic ML. It screened 72 primary works/systems/resources, deeply reviewed
27, and deeply reviewed 24 from 2024--2026. Paper claims and artifacts were
recorded separately.

## 4. Candidate families

A data/analytics; B reliable AI/agents; C software engineering/program systems;
D compiler/runtime; E scientific/optimization; and F fuzzing/security repair.
F was justified by AutoPatchBench, ARVO, SecCodeBench and current security-
repair evaluations with objective fuzz/differential validation.

## 5. Artifact availability

CP-Bench `92ba7dc`, TorchBench `bee9338` and Hybrid-ANNS `ea97ba1` were frozen.
PyTorch 2.13.0+cpu and CPMpy 0.9.25 were installed outside the repository.
CP-Bench ground truths ran. PyTorch compiler execution did not. Hybrid-ANNS,
agent benchmarks and AutoPatchBench required data, containers and/or a current
model route that did not fit a useful pre-gate. See `artifact_metadata.csv`.

## 6. Current benchmark quality

Hybrid-ANNS/RVBench, AutomationBench/SWE-bench Live, TestGenEval, TorchBench,
CP-Bench and AutoPatchBench are substantive public routes. CP-Bench and
AutoPatchBench are especially strong on independent executable correctness.
Benchmark quality did not compensate for absent current-baseline execution.

## 7. Data systems audit

The new PVLDB hybrid evaluation and RVBench justified re-screening structured-
vector execution. The local artifact path was heterogeneous, used separately
hosted datasets and could not produce a bounded fair current comparison. ACORN,
SIEVE, DIGRA and RangePQ already attack the obvious filter/update mechanisms.
No synthetic substitute was introduced. AP1.0's recursive route remained closed.

## 8. Reliable AI audit

AutomationBench, AgentRx and live repository/SQL benchmarks make execution and
recovery more objective. Yet a current agent/model plus traces is part of the
baseline. Paper results and 2025 caches are not a 2026 executable residual.
Verifier/retry/multi-agent wrappers are also heavily occupied prior art.

## 9. Software engineering audit

SAGA, TestGenEval, Vero and SWE-bench provide real repositories and executable
feedback. A current generation system was not available locally, so semantic
or test-quality headroom was not reproduced. Incremental program analysis lacked
a current accepted primary/secondary benchmark pair and collided with mature
caching, demand-driven and incremental approaches.

## 10. Compiler/runtime audit

PyTorch 2.13 was the most executable current systems candidate. The default
locale run failed with an Inductor template decoding error; UTF-8 mode passed
that point and then failed because MSVC `cl` was absent. Neither is a valid
dynamic-shape performance residual. Current PyTorch documentation prefers
automatic dynamics/annotations, and the March 2026 official report states
performance parity on its tested HuggingFace TorchBench and vLLM matrix.

## 11. Scientific/optimization systems audit

CP-Bench supplies natural-language intent, executable models and semantic
solution validation. Three ground-truth workloads ran correctly. The cached
model samples are from May 2025, not a current strong 2026 baseline, so no
current correctness gap was measured. SAT/MaxSAT/XCSP/MiniZinc competitions are
reproducible but generic solver headroom alone is mature and application-weak.

## 12. Optional family

AutoPatchBench contains 136 real fuzz-found C/C++ vulnerabilities (113 Lite)
and verifies build, crash, fuzzing and behavior. ARVO provides the independent
reproducible vulnerability route. The published 2025 case study found roughly
60% generation success but only about 5--11% after full verification, a large
historical gap. Exact current agent execution required dual Linux containers,
fuzzing/LLDB and model access. It is not a finalist or AP-R0-D.

## 13. Executable sanity tests

Five raw rows were retained:

- two PyTorch current-package compiler attempts, both failed before workload
  execution;
- three CP-Bench ground-truth runs, all correct in 1.505--2.059 seconds.

These consumed under 0.05 CPU-hours and 0 GPU-hours. No repeated smoke/hash
ritual or post-hoc benchmark search was performed.

## 14. Semifinal residual experiments

There were **zero semifinals**. D1 did not pass build/run and E1 did not have a
current strong model baseline. Calling either a semifinal would violate the
rule that every semifinal has an executable residual test.

## 15. Strong baseline controls

The frozen D1 control was same-PyTorch eager/static/default/recommended dynamic
execution; it never reached performance measurement. The E1 control required a
current model under the official evaluator; only ground truth was run. `NA`
cells were preserved instead of filling them with historical paper values.

## 16. Mechanism attribution

D1's observed mechanisms were default text decoding and a missing Windows C++
toolchain. They are setup/packaging mechanisms, not the proposed symbolic-shape
runtime mechanism. E1 exposed no failure to attribute. Other candidates did not
pass artifact/current-baseline gates, so mechanisms remain hypotheses only.

## 17. Prior-art collision

The strongest collisions were current PyTorch automatic dynamics, user
annotations, ShapesSpec and 2026 performance fixes; ACORN/SIEVE/DIGRA/RangePQ
for hybrid vector filtering; verifier/retry/test loops for agents; and
AutoPatchBench's own fuzz/differential verifier for security repair. Generic ML
autotuning and "LLM + solver" were not treated as open interventions.

## 18. Engineering burden

E1 was E1--E2; B/C were E2--E3; D1 was E2 on this Windows host; A1 and F1 were
E4 before a fair scientific signal. The grades include artifact and baseline
setup, not only writing a prototype.

## 19. Compute burden

Actual measurement was under 0.05 CPU-hours and zero GPU-hours. A fair A1
multi-system matrix or F1 dual-container fuzzing campaign would remain within
the phase's nominal compute ceiling only after substantial engineering, which
is precisely why they failed the early setup gate.

## 20. Publication ceiling

All six serious directions could support strong venues if they first earned a
residual and a nontrivial intervention. Conditional ceiling is highest for a
general verified repair/execution abstraction, a reusable database execution
method or a compiler abstraction. No venue ceiling changes the present NO-GO.

## 21. Program depth

F1, A1, C1 and B1 have plausible intervention-to-generalization-to-cross-system
trees. D1 also has natural compiler depth, but its targeted gap is current-work
collision. E1 has a plausible semantics-to-interaction tree. Project 2/3 value
does not authorize Project 1 without G5.

## 22. Semifinalists

None.

## 23. Finalists

None.

## 24. Candidate scores

| ID | Direction | Score /90 | Hard result |
|---|---|---:|---|
| D1 | dynamic-shape compilation | 66 | G5/G6/G10 fail |
| F1 | fuzz repair/verification | 64 | G5/G11 fail |
| E1 | semantic constraint synthesis | 63 | G5/G6 fail |
| A1 | hybrid structured-vector execution | 59 | G5/G10 fail |
| C1 | repository test generation | 59 | G5 fail |
| B1 | verified workflows | 58 | G5/G10 fail |

Scores are not ranks because executable gates override them.

## 25. Strongest evidence FOR Rank 1

F1 has the strongest published material gap: real security-critical code,
objective multi-stage verification and a large difference between crash-stopping
and fully verified patches. D1 has the cleanest same-system experimental shape.
These facts justify future evidence collection, not Rank 1 today.

## 26. Strongest evidence AGAINST Rank 1

No candidate passed G5. D1's actual failures disappear into configuration/
toolchain setup and its intended residual is contradicted by a current official
benchmark report. E1 ran only known-correct programs. A/B/C/F lacked a current
strong-baseline execution. Any Rank 1 would therefore be literature-selected,
which is exactly what AP-R0 forbids.

## 27. G1-G14 table

`P` pass, `F` fatal fail, `?` not reached because an earlier gate failed.

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | G9 | G10 | G11 | G12 | G13 | G14 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A1 | P | P | P | P | F | ? | ? | ? | ? | F | F | P | P | P |
| B1 | P | P | P | P | F | ? | ? | ? | ? | F | P | P | P | P |
| C1 | P | P | P | P | F | ? | ? | ? | ? | ? | P | P | P | P |
| D1 | P | P | P | P | F | F | ? | P | F | F | P | P | P | P |
| E1 | P | P | P | F | F | F | ? | ? | ? | ? | P | P | P | P |
| F1 | P | P | P | P | F | ? | ? | ? | ? | ? | F | P | P | P |

## 28. Final decision

**AP-R0-C — NO-GO: STRUCTURED/APPLIED SEARCH SPACE STILL WEAK.** This means
the bounded search failed to identify an earned parent direction; it does not
claim that the six application areas lack open problems.

## 29. Exact next action

After review, expand the search boundary one level beyond these six families in
a new phase, while retaining the same executable-current-residual gate. Do not
perform method development, do not reopen AP1.0, and do not automatically carry
forward D1/F1 as finalists. The next phase should first secure a current
baseline execution route before broad literature scoring.
