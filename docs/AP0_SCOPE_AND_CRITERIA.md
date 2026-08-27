# AP0 scope and decision criteria

## Frozen premise

- Base commit: `475260b6f4fcab5d367d9fadb06239de19263c16`.
- P0-B is preserved: hypergraph theory/algorithms remain viable, but ML is not justified as a necessary primary component. The old hypergraph-theory × ML coupling stays paused.
- AP0 starts from a documented application pain, not from a preferred mathematical object or model family.
- AP0 performs literature, system, benchmark, engineering and venue audits only. No model, optimizer, query engine or solver is built or trained.

## Search boundary

Search date: 2026-08-27. Five prescribed families were audited:

1. structured data/query/execution;
2. structured reasoning and constraint solving;
3. reliable AI with executable/verifiable backends;
4. dynamic/incremental structured computation;
5. structured optimization for reproducible workloads.

No optional sixth family was added: the search did not reveal a distinct application family with better evidence than the prescribed five.

## Evidence levels

- **Screened**: primary paper, benchmark, competition, or maintained system page was inspected for task, date, community and claimed contribution.
- **Deep**: in addition, the problem definition, evaluated workload, strongest comparison, measured residual, artifact status and limitations were extracted.
- A search-result snippet alone is not a deep inspection.
- Vendor claims are never used as sole novelty or performance evidence.

## Early-stop order

Candidates are tested in this order: real pain → public benchmark → closest-prior-art collision → residual against strong baseline → small-team feasibility → 2–3 year depth. A failure at an earlier step blocks method design.

## Scores and gates

The candidate matrix uses the requested 17 axes, each scored 0–5, total `/85`. G1–G12 override the score. A direction can win without ML; AI receives credit only when uncertainty, semantics or workload variation makes a learned component technically necessary.

## Decision threshold

AP0-A requires one direction to pass all hard gates and dominate alternatives on documented residual, evaluation accessibility, small-team feasibility and program depth. The selected item is a parent direction, not a proposed architecture.
