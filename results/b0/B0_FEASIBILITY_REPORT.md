# AHSL Phase B0 Feasibility Report

## 1. Executive decision

Phase B0 asked whether a credible real task justifies learning a shared,
feature-conditioned connected-support prior while preserving meaningful exact
inference.

The answer is:

```text
NO-GO for Phase B1 implementation.
```

No surveyed task simultaneously has real paired data, prediction-time
covariates, a transferable repeated-instance law, a scientifically valid
nonempty connected support, an observed trustworthy scaffold, and a material
need for exact connected-support inference.

This closes the current AHSL machine-learning line after B0. It does not undo
the A-series algorithmic results and does not claim that the surveyed
application domains are unimportant.

## 2. Frozen inherited evidence

The B0 decision inherits the accepted A1.5 result at commit
`930ebc003cbc35a5704e3eb76200b15d0c7a17d3`:

- deployable aligned TreeGain was approximately `0.00093`, with a confidence
  interval crossing zero;
- the non-tied gain was approximately `0.00015`;
- tree-identity learning was therefore stopped;
- decision-aligned posterior decoding retained a small, stable positive signal;
- estimated trees produced posterior overconfidence relative to the generating
  tree.

B0 did not rerun or modify those experiments.

## 3. What B0 investigated

Eight task families were examined through primary papers and official data
records:

1. biomedical semantic indexing with MeSH;
2. protein binding-residue prediction;
3. phylogenetic placement;
4. radial power-grid outage/fault localization;
5. pulmonary embolus localization;
6. coronary and retinal vessel tasks;
7. fish occupancy on dendritic stream networks;
8. infection cascades and transmission trees.

The review explicitly separated four questions that are often conflated:

- Is the task real?
- Is some tree or branching geometry present?
- Is the *label support* correctly modeled as one nonempty connected set?
- Does exact inference over that set solve a practical bottleneck?

## 4. Candidate results

| Candidate | Strongest positive evidence | Controlling failure | Decision |
| --- | --- | --- | --- |
| BioASQ/MeSH | Millions of real articles; prediction-time text; curator labels | Multi-path DAG multilabel task; closer mature formulation; connectivity can be vacuous | NO-GO |
| Protein binding | Real 3D structures and residue labels | Natural scaffold is a cyclic spatial graph; multiple sites | NO-GO |
| Phylogenetic placement | Known reference tree; extreme exact-likelihood throughput need | Output is one edge or alternatives over edges, not a connected support | NO-GO |
| Grid outage/fault | Radial structure; real-time sensor use; connected downstream region plausible | No identified public real topology-sensor-event-label dataset | CONDITIONAL HOLD at task level; B0 NO-GO |
| Pulmonary emboli | Large public CTPA data; artery-level boxes in an augmented subset | Multiple/empty supports; patient arterial tree absent; object detection is natural | NO-GO |
| Coronary/retinal vessels | Real tree segmentations and centerlines | Tree is the prediction target; patient-specific structure | NO-GO |
| Stream fish occupancy | Real occurrence, covariates, and topologically accurate networks | Fragmentation and absence are biological outcomes | NO-GO |
| Transmission/outbreaks | Real reconstructed trees and heterogeneous covariates | Tree is latent; missing cases disconnect observations; phylogeny is not transmission tree | NO-GO |

## 5. The closest case and why it still cannot proceed

Radial-grid outage localization is the only candidate where a single real event
on a known radial feeder can naturally generate a downstream connected region,
and where fast calibrated inference could plausibly aid operations.

However, B0 found a decisive data split:

- detailed public feeder resources such as SMART-DS are explicitly synthetic;
- real smart-meter trials exist but do not release a reusable pairing of
  event-time topology, measurements, and line/device ground truth.

Training on simulated faults, even with real load traces, would not answer the
real-task question. It would recreate the generator-matched loop that motivated
B0. Therefore this candidate cannot authorize code.

## 6. Why the data-rich candidates do not combine into a pass

The negative result is not caused by data scarcity alone:

- BioASQ has excellent data but its natural target is a DAG-structured
  multilabel set and already has direct structured-prediction methods.
- RSPECT has excellent imaging data but multiple bilateral emboli and negative
  studies violate a nonempty single-component output; the patient arterial tree
  is not supplied.
- stream ecology has real topology and covariates, but fragmentation is a
  scientific signal rather than noise to be projected away.
- BioLiP has real residue labels, but the natural geometry is a spatial graph,
  not a tree.

Choosing a dataset from one row and a structural assumption from another would
not produce a coherent task.

## 7. Tractability finding

Exact inference is demonstrably important in phylogenetic placement and
probabilistic transmission analysis, but those computations concern different
latent objects. Conversely, the data-rich classification and imaging tasks do
not identify connected-subtree marginalization as their limiting computation.

Thus B0 found no case where AHSL's exact DP is simultaneously:

1. exact for the correct domain output class;
2. fed by a real learnable conditional prior;
3. operationally or statistically material.

## 8. Structural uncertainty finding

Most visually appealing candidates make the scaffold uncertain:

- arterial and coronary trees are patient-specific and must be extracted;
- feeder topology can change with switching and may be incompletely recorded;
- transmission trees are reconstructed under missing cases;
- projecting protein contacts or MeSH DAGs to trees is a modeling choice.

Conditioning on these structures as if they were correct would reproduce the
estimated-tree overconfidence seen in A1.5. Exact inference conditional on a
misspecified tree does not provide calibrated uncertainty about the real task.

## 9. Scientific interpretation

B0 supports a narrower conclusion than “connected structural priors are never
useful.” The evidence supports:

```text
No currently identified public real task justifies extending this AHSL model
line under its frozen output and inference assumptions.
```

This is the appropriate stopping claim. Broader negative claims would exceed
the search evidence.

## 10. Reopening condition

The line may be reconsidered only when an external real dataset, not a new
synthetic generator, satisfies all B0 gates. The grid candidate provides the
clearest concrete condition: real events, prediction-time meter data, event-time
topology, line/device ground truth, enough independent events, and publishable
access.

If such data arrive, the first activity is a data-only audit of empty,
multi-component, topology-consistency, and scaffold-uncertainty rates. It is not
model training and does not revive tree-identity learning.

## 11. Final route status

| Research direction | Status after B0 |
| --- | --- |
| Fixed-tree exact DP and posterior infrastructure | Retain as completed infrastructure |
| Tree-identity learning | STOP, unchanged |
| New synthetic subtree estimators | STOP |
| Shared/feature-conditioned subtree prior | NO-GO for implementation |
| GHW greater than one | Not started |
| Radial-grid task | External-data conditional hold only |
| Current AHSL ML line | STOP after B0 |

## 12. Artifacts

- Gate definition: `docs/B0_SCOPE_AND_GATE.md`
- Candidate analysis: `docs/B0_APPLICATION_SURVEY.md`
- Data/tractability audit: `docs/B0_DATA_AND_TRACTABILITY_AUDIT.md`
- Search record: `docs/B0_SEARCH_LOG.md`
- References: `references/b0_references.bib`
