# N1.0 theory audit

## 1. Directed hyperpath semantics

Let (H=(V,E)) be a finite directed hypergraph. Each reaction (e\in E) has a nonempty tail (T(e)\subseteq V) and nonempty head (H(e)\subseteq V). Given sources (S\subseteq V), an edge set (P\subseteq E) is a feasible superpath to target set (U\subseteq V) when its edges admit an ordering (e_1,\ldots,e_k) such that (T(e_i)\subseteq S\cup\bigcup_{j<i}H(e_j)), and (U\subseteq S\cup\bigcup_{j\le k}H(e_j)). Equivalently, all targets are B-connected from (S) using only (P).

Following Mmunin, a hyperpath is an inclusion-minimal feasible superpath. Cycles and self-loops may occur in the ambient hypergraph; feasibility is determined by forward closure, not by an acyclicity restriction. A synthetic sink fed by one hyperedge whose tail is the declared target set converts a conjunctive multi-target query to the single-target form without weakening AND semantics.

## 2. Additive positive reaction-cost objective

For strictly positive reaction costs (c_e>0), the deployed objective is

\[
C_c(P)=\sum_{e\in P} c_e,
\qquad P\in\mathcal F(S,U),
\]

where \(\mathcal F(S,U)\) is the finite family of feasible edge sets. Positive additivity means that retaining a redundant reaction always increases cost.

## 3. Gold feasibility

A curated reaction set (P^*\) is gold-feasible when (U) is in the forward closure of (S) under (P^*\). This is a necessary condition for exact recovery under any cost vector. It is not a model-performance statistic: infeasible labels lie outside the decoder's output class.

## 4. Positive-cost attainability

**Definition.** A gold set (P^*\in\mathcal F(S,U)) is positive-cost attainable if there exists a vector (c\in\mathbb R_{>0}^{E}) for which (P^*\) is the unique minimizer of (C_c) over \(\mathcal F(S,U)\).

**Theorem.** In a finite directed hypergraph under the Mmunin feasible-superpath semantics, (P^*\) is positive-cost attainable if and only if no feasible (Q\subsetneq P^*\) exists.

## 5. Necessity proof

If a feasible (Q\subsetneq P^*\) exists, then for every strictly positive (c),

\[
C_c(P^*)-C_c(Q)=\sum_{e\in P^*\setminus Q}c_e>0.
\]

Thus (P^*\) cannot even be optimal, let alone uniquely optimal.

## 6. Sufficiency proof

Assume no feasible proper subset of (P^*\) exists. Set (c_e=\varepsilon) for (e\in P^*\) and (c_e=1) otherwise, with (0<\varepsilon<1/|P^*|). Every distinct feasible (Q) must contain an edge outside (P^*\); otherwise it would be a forbidden feasible subset. Hence (C_c(Q)\ge1), while (C_c(P^*)=|P^*|\varepsilon<1). Therefore (P^*\) is uniquely optimal.

The argument also covers feasible superpaths that are not minimal. Because costs are positive, any nonminimal feasible set is dominated by a feasible proper subset. The theorem therefore agrees with Mmunin's minimal-hyperpath interpretation.

## 7. Exact attainability test

Restrict (H) to (P^*\). Then either:

- solve the minimum-cardinality exact hyperpath problem and compare its optimum with (|P^*|); or
- for each (e\in P^*\), test exact forward reachability after deleting (e).

The second form is exact here: if any feasible (Q\subsetneq P^*\) exists, choose (e\in P^*\setminus Q); then (P^*\setminus\{e\}) is still feasible by monotonicity. Conversely, a feasible one-edge deletion is itself a proper-subset witness. The production audit used this exact deletion characterization after a full minimum-cardinality cut-plane run proved unnecessarily slow. The classification is exact, although minimum sizes for rejected labels were not computed.

Exhaustive enumeration on 64 small hypergraphs produced 1,847 feasible gold sets and zero decision mismatches; the MILP minimum-cardinality check also had zero mismatches on the validated cases.

## 8. Limitations of attainability

Attainability says only that some positive additive vector can encode the label. It does not establish biological truth, identifiability of costs, predictive learnability, causal interpretation, or robustness. The constructive costs depend on the gold set and are not a learning algorithm. A pathway may be attainable but biologically redundant; conversely, a curated set may be biologically meaningful yet unattainable because annotation intentionally retains branches.

## 9. Robust interval optimality margin

Suppose costs satisfy independent intervals (c_e\in[\ell_e,u_e]). For a candidate (P) and competitor (Q), the worst-case cost gap is

\[
\min_c\{C_c(Q)-C_c(P)\}
=\sum_{e\in Q\setminus P}\ell_e-\sum_{e\in P\setminus Q}u_e.
\]

Define modified weights (w_e=u_e) for (e\in P) and (w_e=\ell_e) otherwise. The robust margin is

\[
\Delta(P)=\min_{Q\ne P,\ Q\in\mathcal F} \sum_{e\in Q}w_e-\sum_{e\in P}u_e.
\]

If \(\Delta(P)>0\), (P) remains uniquely optimal for every cost vector in the box.

## 10. Second-best competitor formulation

The margin reduces to a second exact solve with weights (w), but the exclusion must remove all supersets of (P), not merely the identical binary vector. Add

\[
\sum_{e\in P}x_e\le |P|-1.
\]

Every distinct minimal hyperpath omits at least one edge of (P). A conventional no-good cut for (x\ne 1_P) would allow (P\cup\{e}); under superpath variables that nonminimal set can create an artificial competitor. The superset-exclusion inequality is therefore the correct Mmunin-compatible formulation.

## 11. Statistical calibration versus deterministic certification

Statistical intervals estimate uncertainty under a data-generating process; the box certificate is a deterministic statement conditional on supplied intervals. Marginal reaction-wise coverage does not imply simultaneous coverage of the full cost vector. No continuous true reaction cost is observed in Reactome, so cost calibration would itself require a defensible target or conformal construction. The certificate must not be described as calibrated merely because it uses intervals.

## 12. What is classical

Directed-hypergraph reachability, shortest hyperpaths, inverse shortest paths, interval robust shortest paths, exact MILP/cut generation, and the algebraic robust-margin reduction are classical optimization components. N1.0 claims no new solver theorem beyond specializing and checking these facts against the proposed task semantics.

## 13. What remains only a future ML hypothesis

Learning context-dependent reaction costs, estimating valid joint uncertainty sets, improving pathway-set F1 over exact handcrafted baselines, and obtaining useful abstention coverage remain untested hypotheses. N1.0 does not authorize them: the natural-universe attainability rate is 59.32%, below the frozen 70% gate.
