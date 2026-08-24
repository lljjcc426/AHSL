# A1 Literature Review

Search date: 2026-08-25

## Scope and conclusion

This review covers alpha-acyclic hypergraphs, join/junction-tree learning,
latent and noisy tree models, random connected subtrees, exact tree
marginalization, Structural EM, structured spanning-tree prediction, modern
hypergraph structure learning, and hypertree-width methods.

The literature gate is **MODIFY**. The proposed model is not substantially
subsumed by one located paper, but most of its algorithmic ingredients are
classical. A1 can test a narrow statistical synthesis; it cannot claim a new
connected-subtree DP, a first marginal-likelihood tree learner, or a first noisy
tree-recovery method.

## A. Alpha-acyclicity and join trees

Beeri, Fagin, Maier, and Yannakakis (1983) established the central equivalent
characterizations of acyclic database schemes. Fagin (1983) separated alpha,
beta, and gamma acyclicity. Yannakakis (1981) and Tarjan and Yannakakis (1984)
gave the classical algorithmic foundations for acyclic schemes and linear-time
recognition/reduction.

For AHSL, the crucial point is nonuniqueness. A join tree is a certificate that
the set of hyperedges containing each vertex is connected, not necessarily a
unique latent identity. The weighted line-graph maximum-spanning-tree
characterization explains the A0.75 baselines. Berry and Simonet (2021) and
Leitert (2021) make nonuniqueness explicit through the union join graph, the
union of all possible join-tree edges.

Implication: edge recovery cannot be the primary endpoint; held-out likelihood
and recovery are more scientifically aligned.

## B. Learning hypertree and junction-tree structures

Borgelt and Kruse (2001) directly optimize graphical models constrained to
hypertree structure with simulated annealing, limiting maximal clique size so
that join-tree evidence propagation remains tractable. Their nodes are random
variables and their hypertree nodes are maximal cliques of a decomposable
graphical model. AHSL instead fixes observed hyperedge columns as tree nodes and
uses original hypergraph vertices as iid rows whose latent supports are
connected. The shared idea is learning under a tractability constraint; the
statistical object and likelihood are different.

Karger and Srebro (2001), Kumar and Bach (2013), and Nie, de Campos, and Ji
(2016) further show that maximum-likelihood or score-based bounded-treewidth
structure learning is established and generally combinatorial. Thomas and Green
(2009) show that junction-tree representations of one decomposable graph are
themselves nonunique and can be enumerated/sampled.

Implication: "learning a tractable tree/junction structure from data" is not a
novel claim. AHSL's remaining distinction must be its hypergraph-incidence
latent support model and certificate.

## C. Latent and noisy tree graphical models

Chow and Liu (1968) recover a maximum-likelihood dependence tree from complete
samples by a maximum-weight spanning tree. Choi et al. (2011) learn minimal
latent tree graphical models using information distances, recursive grouping,
and an MST-guided global step. Huang et al. (2020) provide scalable recovery
guarantees for broad linear latent-tree families.

Nikolakakis, Kalogerias, and Sarwate (2019) analyze Ising and Gaussian tree
recovery from noisy samples and show that noise changes sample requirements but
does not make "noisy tree learning" a new problem. Felsenstein's (1981)
phylogenetic maximum-likelihood work is an important historical example of
exact likelihood evaluation followed by tree-topology search. Zwiernik (2011)
also warns that hidden tree models can be singular, so generic regular-model
criteria such as ordinary BIC need care.

These works place random variables at tree nodes or leaves. AHSL places labeled
hyperedges at tree nodes and constrains the latent one-set of each iid row to be
connected. The distinction is real, but narrower than a generic latent-tree
claim.

## D. Random connected subtrees

The AHSL generator has a standard interpretation: Bernoulli bond percolation on
a fixed finite tree, followed by selection of the open component containing a
uniform vertex. The resulting cluster law is size-biased by component size.
Fredes and Marckert (2021) survey multiple random-subtree models, while Moon
(1997) and Tittmann, Averbouch, and Makowsky (2011) study enumeration and
generating functions for induced connected subgraphs.

No located source used exactly the AHSL observation model and tree-selection
objective. Nevertheless, independent edge opening and sampling a containing
cluster are established probabilistic constructions. A1 therefore names and
cites the percolation interpretation instead of presenting the prior as a new
random-subtree family.

## E. Exact marginalization over connected subtrees

Kschischang, Frey, and Loeliger (2001) give the general sum-product framework:
on a cycle-free factor graph, marginalization of a product of local factors is
exact. The proposed `E/I` recurrence is precisely such a specialization.
Felsenstein's pruning algorithm is another domain-specific tree likelihood
recursion.

Chen and Yuille (2015) are especially close at the state-space level: visible
object parts are constrained to form a connected subtree, and inference shares
work across exponentially many flexible compositions. Their objective and
emissions are vision-specific and they do not learn the underlying labeled tree,
but their work blocks any claim that efficient inference over all connected
subtrees is new.

The connected-subgraph polynomial literature also treats partition functions
over induced subgraphs and establishes hardness on general graphs and
tractability under structural restrictions.

## F. Latent-variable structure learning

Friedman (1997, 1998) introduced Structural EM and Bayesian Structural EM for
learning model structure from incomplete or hidden data. The framework computes
expected sufficient statistics under a current model and searches for an
improved structure, with monotonicity/convergence results under its assumptions.

AHSL belongs to this broad family, but a literal structural step is not
automatically advantageous. Candidate trees change which support sets are
feasible. A support with positive posterior under the current tree can have zero
probability under a proposed tree, so the usual common-completion structural
score is not a simple MST objective. Exact observed-data likelihood scoring is
available at `O(nm)` per candidate and is the cleaner small-scale approach.

## G. Structured spanning-tree prediction

Koo et al. (2007) compute partition functions and marginals over directed
spanning trees with the Matrix-Tree Theorem. Kim et al. (2017) embed structured
tree distributions as differentiable attention. Paulus et al. (2020) construct
continuous relaxations for spanning trees, and Corro and Titov (2019) use
differentiable dynamic programming for latent projective trees.

These methods concern future amortized or task-driven learning. They do not
justify neural A1: the current model has an exact classical likelihood and a
small scalar prior parameter.

## H. Modern hypergraph structure learning

Cai et al. (2022) optimize hyperedge and incident-node sampling jointly with an
HGNN for downstream tasks. Badalyan, Ruggeri, and De Bacco (2024) use a
probabilistic hypergraph/community model with node attributes and missing-edge
prediction. Li et al. (2025) learn soft hypergraph incidence by self-supervised
contrastive objectives. Wen and Yu (2025) generate hypergraphs by projection,
latent graph learning, and clique-cover reconstruction.

These methods target predictive representation, community inference, or
generation. They generally output soft/learned topology and do not enforce a
join-tree certificate. AHSL's tractability-certified output is therefore a real
distinction. Conversely, AHSL currently lacks their realistic features,
downstream tasks, and scale, so it cannot claim broader practical superiority.

## I. Hypertree width, GHW, and FHW

Gottlob, Leone, and Scarcello (2002) introduced hypertree decompositions and
hypertree width for tractable conjunctive queries. Grohe and Marx (2006)
introduced fractional hypertree width, and Marx (2013) placed these notions in a
broader complexity classification. Gottlob et al. (2024) improve practical
hypertree-decomposition computation with logarithmic recursion depth and
parallel search.

This literature supports a possible wider bounded-width program, but not an
automatic jump from `k=1` to `k>1`. If A1 fails because tree identity has little
held-out value or because incidence structural regularization is unhelpful,
larger width is not justified. A GHW continuation would require evidence that
alpha-acyclicity itself is the binding misspecification.

## Five closest works and overlap assessment

The detailed comparison is in `A1_CLOSEST_PRIOR_ART.md`. No single work matches
all of noisy incidence, latent connected supports, exact marginalization,
labeled-tree selection, and alpha-acyclic certification. The strongest novelty
threat is the combination of three established lines: connected-subtree exact
inference (Chen and Yuille; sum-product), latent structure learning (Friedman),
and noisy tree recovery (Nikolakakis et al.).

## Literature-based stop rule

The stop rule is not triggered before implementation because no screened paper
substantially subsumes the end-to-end statistical problem. It would be triggered
by claims of a novel DP or generic latent-tree learner; those claims are removed.

