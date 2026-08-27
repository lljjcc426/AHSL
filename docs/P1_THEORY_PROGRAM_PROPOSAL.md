# P1 theory program proposal

## Program title

**Certified reusable hypertree decompositions for evolving query and constraint
hypergraphs**

## Decision boundary

This proposal follows P0-B. Hypergraph algorithms/theory is primary. ML is
optional and is not part of the initial contribution, benchmark or kill-test.
The proposal does not reopen AHSL, CertPath, S1, S2, S3 or R0.

## Core mathematical objective

For a hypergraph that represents conjunctive-query atoms or CSP scopes, compute
and maintain a verifiable HD/GHD/FHD witness under rerooting and local structural
updates, while controlling width increase, recourse, representation size and
recomputation time.

The native objects are:

- edge covers and fractional edge covers;
- HD/GHD/FHD validity and width;
- running-intersection and normal-form constraints;
- equivalent/rerootable decomposition families;
- update sequences on vertices, hyperedges and scopes.

## Program sequence

### P1.1: canonical and rerootable witness structure

Question: which decomposition equivalences admit a succinct canonical or
rerootable representation without unacceptable width increase?

Deliverables: definitions, separation examples, verifier, exact small-instance
enumerator and theorem/counterexample results.

### P1.2: update-sensitive decomposition maintenance

Question: under local scope changes, what trade-off is possible among width
inflation, recourse and update time?

Deliverables: upper/lower bounds, a certified update algorithm and comparison
with full recomputation on a bounded HyperBench change protocol.

### P1.3: certified downstream relevance

Question: when do reusable/rerootable decompositions preserve or improve CQ/CSP
evaluation, independent of engine-specific heuristics?

Deliverables: structural-to-execution hypotheses, matched decomposition
certificates and a bounded downstream evaluation. This phase starts only after
P1.1/P1.2 establish a nontrivial structural result.

## Benchmarks and verification

- Primary structural corpus: public HyperBench CQ/CSP hypergraphs.
- Second route: versioned XCSP or public conjunctive-query scope families with
  declared licenses and conversion.
- Synthetic instances: permitted only for minimal counterexamples and scaling
  controls, never as the sole evidence.
- Every decomposition is checked for edge coverage, connected vertex
  occurrence and declared cover/width semantics.

## Strongest threats

- exact/parallel HD and GHD algorithms;
- LP-based FHD/GHD approximations;
- new FPT parameterizations by width, rank and degree;
- existing incremental GHD maintenance;
- 2026 rerootable decomposition definitions.

The program is viable only if its first statement is not a direct restatement
or engineering combination of those works.

## First bounded kill-test

1. Freeze one of: canonical representation, rerootability-width trade-off, or
   update recourse.
2. State one theorem target and one falsifying construction.
3. Reconcile definitions with the five strongest recent decomposition works.
4. Use an exact verifier/enumerator on minimal instances and at most a small,
   declared HyperBench subset.
5. Stop if the statement is a direct corollary, if only runtime engineering
   remains, or if the native hypergraph formulation reduces without loss to a
   known treewidth result.

## ML admission rule

An ML heuristic may enter only after a classical algorithmic residual is
measured on repeated update families and a pre-update feature map predicts it
across held-out families. It may rank moves but cannot define validity. This is
a later optional gate, not a planned project requirement.

## Compute and publication fit

The first phase is theorem- and verifier-centered and fits ordinary CPU
resources. Natural communities are database theory, algorithms, CSP and
parameterized complexity. Plausible publication value comes from a new theorem
or certified algorithm, not from adding a learner.

## Exact next action

Prepare a P1.1 definition-and-prior-art note that chooses exactly one theorem
target and proves or refutes it on minimal instances before any performance
implementation.
