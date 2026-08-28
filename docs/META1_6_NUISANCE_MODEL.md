# META1.6 nuisance model

Three formulations were separated before outcome evaluation.

1. N0: dense, unpenalized low-order nuisance, eliminated by orthogonal projection. It is structurally impossible at budget 16 and highly constrained at 24/32.
2. N1: joint sparse penalization of all 63 nonempty terms, with evaluation restricted to the 42 high-order targets.
3. N2: ridge residualization of the low-order block, retained only as a regularization sensitivity because its answer depends on the ridge strength.

N1 is frozen as primary. This explicitly assumes approximate joint sparsity; it does not disguise the N0 failure. No heredity assumption is used. The empty-row response anchors the omitted constant term; the primary working model treats resulting errors as homoscedastic, which is a declared approximation rather than a claim about replicate biology.
