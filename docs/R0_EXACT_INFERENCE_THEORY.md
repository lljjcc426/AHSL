# R0 Exact-Inference Theory

## Semiring elimination

For factors `psi_e(x_e)`, partition and marginal computation repeatedly applies
distributivity:

`Z = sum_x product_e psi_e(x_e)`.

Eliminating variable `v` combines all factors whose scopes contain `v` and
aggregates over `v`. Every complete order gives the same exact answer. It does
not give the same cost: the union of incident scopes becomes an intermediate
factor, and its dense entries equal the product of the participating domain
sizes.

Bucket elimination, junction-tree propagation, recursive conditioning and
AND/OR search are different organizations of this exact computation. Their
resource bounds depend on an order, tree decomposition or pseudo-tree.

## Structural measures

Primal-graph induced width controls dense table elimination. Native hypergraph
measures can be smaller: a single scope `V` has `ghw=1`, while its primal graph
is a clique with treewidth `|V|-1`. This separation only helps when the factor is
already given compactly or sparsely; a dense table over `V` still has
`prod_v |D_v|` input entries.

For sparse listing representations, a bag computation can be treated as a
multiway join. Fractional edge covers and FAQ/FHD widths then bound support
processing more sharply than pairwise dense products. The execution cost still
also depends on support cardinalities, domain sizes, constants, messages and
the chosen implementation.

## Correctness contract

- Any complete VE order is exact.
- A predicted junction/GHD decomposition must pass the running-intersection,
  edge-coverage and guard conditions before use.
- A predicted solver configuration is safe only when every selected engine is
  exact for the requested task.
- A learned pruning score may rank nodes, but pruning needs an independently
  admissible bound or exhaustive fallback.

Thus certificate-by-construction is clean. The unresolved question is whether
the safe strategy choice has enough non-classical, learnable headroom.

## Cost metric used in R0

The structural audit reports induced width, maximum union arity, peak dense
entries and total joined entries. The bounded exact audit reports wall time and
verifies order-invariant partition values. These metrics do not claim exact
GHW/FHW and do not substitute structural proxies for actual runtime.
