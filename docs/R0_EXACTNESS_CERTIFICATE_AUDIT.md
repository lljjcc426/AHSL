# R0 Exactness and Certificate Audit

| candidate decision | learner may get wrong | deterministic protection | answer remains exact? | cost failure mode |
|---|---|---|---:|---|
| VE order | chooses a poor permutation | execute every variable exactly once | yes | huge intermediate table/time |
| junction-tree order | poor triangulation/root | verify tree and running intersection; exact propagation | yes | width/memory blow-up |
| GHD/FHD proposal | invalid bags/guards/covers | deterministic coverage, connectedness and width verification; fallback search | yes after verification | verifier/search overhead or poor width |
| local separator/bucket move | myopic move | move only affects a complete exact plan | yes | later fill-in |
| solver portfolio | selects slow engine | restrict portfolio to exact engines and validate task compatibility | yes | timeout; optional parallel/racing fallback |
| plan-cost prediction | inaccurate cost | use prediction only for ranking; execute selected exact plan | yes | regret relative to analytic heuristic |
| branch priority | poor node choice | complete branch-and-bound/search | yes | larger search tree |
| pruning bound | optimistic/non-admissible learned score | never prune without independent admissible certificate | yes | learned score may only rank |

The cleanest R0 architecture is order/portfolio prediction because correctness
is semantic and independent of prediction. Decomposition proposals need a
verifier. Safe pruning is narrower: a learned bound cannot itself authorize
pruning.

The local exact implementation checked the core contract directly: four
different elimination strategies returned the same partition value for each
executed UAI model, while costs differed. The test suite also covers a
three-variable factor model under two distinct orders.

Exactness cleanliness passes G9, but it is not novelty. Generic CP, SAT,
database and tensor systems already use the same “heuristic affects cost, exact
engine affects correctness” separation.
