# F1-D1 cost audit

Repair-baseline model calls, tokens, model cost, verifier time, fuzz time, and container time are all zero because infrastructure sanity failed before candidate generation. The single agent-access probe used one ephemeral call and reported 6,366 tokens; it is excluded from repair outcomes.

The ledger supports prompt/completion tokens, model calls, provider cost, verifier seconds, fuzz seconds, and wall time. Equal-budget checks compare full `RepairBudget` objects, not only nominal attempts. Future V4 gains must be reported with paired cost deltas.
