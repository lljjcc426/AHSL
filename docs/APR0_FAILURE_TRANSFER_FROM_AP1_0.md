# AP-R0 failure transfer from AP1.0

AP1.0 established AP1.0-C / R7: the successfully executed current same-engine
matrix did not expose an actionable recursive incremental residual. All eleven
FlowLog cells were exact and incremental execution was 2.560--8.953x faster
than scratch; maximum valid update-peak ratio was 1.969x, below the frozen 2x
gate. Missing internal state counters were not replaced by RSS speculation.

The transferable lesson is not that systems work is exhausted. It is that a
published historical bottleneck can disappear in a current implementation.
Consequently AP-R0:

1. uses current releases/artifacts before direction ranking;
2. requires same-system controls where possible;
3. treats obvious configuration and toolchain setup separately from a scientific
   residual;
4. retains negative cells and stops when G5 is absent;
5. does not promote an AP0 runner-up by default.

New 2025--2026 vector-relational evidence (the PVLDB hybrid evaluation and
RVBench) justifies re-screening that family, but its multi-system artifact and
separate datasets did not become a bounded current executable route here. That
is re-screening, not reopening AP1.0.
