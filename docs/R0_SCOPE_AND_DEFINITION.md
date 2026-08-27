# R0 Scope and Definition

## Interface

R0 fixes a discrete factor/CSP hypergraph `H=(V,E)` and factor data
`{psi_e}`. A learned component may propose an elimination order,
decomposition move, local separator, solver, plan or priority. A deterministic
exact engine still computes the partition function, marginals, MAP/MPE or CSP
answer. Prediction error may increase runtime or memory; it may not change the
answer or invalidate a certificate.

The project therefore studies cost selection

`known instance -> proposed strategy -> exact execution -> certified answer`,

not structure learning and not amortized approximate inference.

## Inclusion boundary

The representation is genuinely high-order only when at least one native
factor/constraint scope has arity at least three and its compact/sparse/table
representation is recorded. A large scope is not automatically tractable:
input table size, domain cardinality, support sparsity and deterministic zeros
must accompany width claims.

The following remain out of scope: learning `H`, approximate neural marginals,
generic SAT branching, generic query optimization, generic tensor contraction,
and a decomposition label without downstream exact-inference benefit.

## Candidate problems screened

1. variable/factor elimination ordering;
2. verified GHD/FHD decomposition search;
3. local separator/bucket/elimination decisions;
4. exact-engine/configuration portfolios;
5. execution-cost prediction for candidate plans;
6. safe learned proposals with deterministic fallback.

## Frozen empirical threshold

Before reading R0 strategy results, the prompt supplied the diagnostic gate:
median worst/best feasible runtime ratio at least `3x`, or a timeout-rate gap of
at least 20 percentage points, on two benchmark families. “Feasible strategy”
means a serious classical candidate, not an intentionally bad random order.

## Outcome boundary

Random orders prove that strategy can matter in principle, but the bounded UAI
audit did not show a `3x` residual among min-fill, weighted min-fill,
min-degree and a domain/factor-size-aware greedy order on two families. The
remaining apparent opportunity is engine/configuration/branch selection, which
is already the generic interface of CP/SAT, database and tensor-network solver
learning. R0 therefore does not authorize R1.
