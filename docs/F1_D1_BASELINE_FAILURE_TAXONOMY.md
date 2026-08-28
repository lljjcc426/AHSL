# F1-D1 baseline failure taxonomy

Terminal classes F0–F9 are implemented exactly as protocol states: no patch, build failure, original crash persists, fuzz failure, differential failure, ordinary-test regression, symptom-only patch, context outside scope, exhausted budget, and infrastructure/evaluator failure. Fully verified is separate.

The current ledger contains 25 F9 preflight exclusions and zero scientific repair trajectories. Consequently there is no dominant repair failure stage or semantic subclass yet. F9 must not be used to select an intervention.

Once the sanity set runs, each baseline trajectory will retain its complete V0–V4 path. F3/F4/F5 cases will then receive one evidence-based semantic label; failures will not be deleted.
