# AP0 AI/ML collision audit

## Database + AI saturation

Learned cardinality estimation, learned cost models, join-order prediction, index recommendation and LLM query rewriting are established lines. AP0 therefore rejects “learn a better recursive-query cost” as a parent direction. A learned component becomes justified only after AP1 demonstrates a repeated decision whose optimal choice depends on unmodeled update/query distributions and whose bad choices survive strong classical adaptive policies.

## Reliable text-to-SQL collision

| Work | Occupied component | Consequence |
|---|---|---|
| execution-guided decoding | reject candidates that fail execution | execution success alone is old and cannot establish semantic correctness |
| CHESS (2024) | schema/value retrieval, schema pruning, iterative generation, LLM unit tests | generic retrieval + testing + multi-agent framing is occupied |
| CHASE-SQL (2024) | diverse multi-path candidates and learned pairwise selector | candidate diversity/selection is occupied |
| Spider-Agent/Spider 2.0 | environment interaction over enterprise workflows | “agent uses database tools” is benchmark baseline, not novelty |
| CEDAR (2025) | cost-aware routing among iterative claim-to-SQL verification methods | cost/accuracy routing and claimed-value-aware verification are occupied |
| LiveSQLBench/BIRD-Interact | changing and interactive evaluation | static Spider/BIRD gains alone have a declining ceiling |

A surviving reliable-AI project must introduce at least one of: a semantic specification that can distinguish plausible wrong SQL, a nontrivial certified repair algorithm, a new exact execution architecture, or guarantees about valid completion/cost. Prompt chains and output filters fail the gate.

## LLM + solver collision

CP-Bench already evaluates LLM generation for MiniZinc, CPMpy and CP-SAT. SMT/CP tool use and iterative repair are increasingly common. “LLM proposes, solver says feasible” is especially weak because feasibility does not establish that the generated model represents the user's intent.

## AI role in the winner

No AI is required for the first project. A later learned component is credible only for:

1. predicting update/query regimes not available analytically;
2. selecting among already-correct execution/state policies;
3. preserving exact output under a deterministic fallback;
4. demonstrating benefit beyond a robust rule-based adaptive policy.

The direction remains valuable if all four opportunities fail; this is a positive property, not a missing component.
