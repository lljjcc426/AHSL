# R0 Literature Landscape

| line | exactness | native high-order role | strategy issue | closest collision | R0 outcome |
|---|---:|---|---|---|---|
| variable/bucket elimination and junction trees | yes | factor scopes induce intermediate scopes | ordering controls induced width/table cost | treewidth heuristics | classical residual not established |
| AND/OR search and recursive conditioning | yes | constraints/factors define decomposition | pseudo-tree, caching and branch order | generic graphical-model search | generic solver guidance |
| HD/GHD/FHD inference | yes when decomposition and operations are verified | guards/edge covers directly use hyperedges | finding a useful decomposition is hard | CSP/query decomposition | benchmark lacks paired factor execution |
| FAQ and worst-case optimal joins | yes over the declared semiring | fractional covers bound joins | variable ordering/decomposition/join implementation | database query planning | near-identity collision |
| JoinInfer | yes | sparse high-arity factors can favor GHD/WCOJ execution | per-bag method and engine selection | data-driven hybrid already present | strongest FOR and strongest prior collision |
| CP/XCSP solving | yes/certified | native global and extensional constraints | propagation, branching, restart, portfolio | mature learned CP/SAT policies | high-order theory optional in surviving task |
| tensor contraction planning | exact up to numerical arithmetic | tensors are high-order factors | contraction tree controls FLOPs/memory | cotengra and RL-TNCO | ordering candidate is not distinctive |
| learned query optimization | database semantics | join hypergraph and cardinalities | cost/cardinality/plan prediction | mature learned optimizers | cost-model candidate is cosmetic |
| learning-augmented algorithms | usually preserves fallback guarantees | problem dependent | consistency, robustness, prediction error | online/scheduling/caching theory | clean contract, but no R0-specific residual |

The exact-inference foundations are mature, and recent GHD/FHD theory is active.
What is missing is not a way to phrase a safe learned proposal. It is a real,
family-disjoint benchmark demonstrating that classical strategies leave a
predictable, hypergraph-specific residual.
