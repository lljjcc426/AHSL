# Phase B0 Data, Structure, and Tractability Audit

## 1. Dataset-level audit

| Resource | Real inputs | Real labels | Scaffold supplied at label resolution | Repeated instances | Main blocker |
| --- | --- | --- | --- | --- | --- |
| BioASQ/MEDLINE | Yes | Yes, curator MeSH | Fixed MeSH DAG/forest, not one tree | Millions | Natural target is multi-path hierarchical multilabel |
| BioLiP | Yes | Yes, binding residues | 3D structure supplied; natural graph is cyclic | Large | Label geometry is not a tree support |
| EPA-ng empirical sets | Yes | Placement evaluated on real sequences | Fixed reference phylogeny | Large | Target is one edge/distribution over edges |
| SMART-DS | No: synthetic networks and loads | Simulated event labels only | Yes | Large | Explicitly synthetic |
| Real utility smart-meter trials | Yes | Sometimes internally | Not released as reusable paired data | Potentially large | Access/proprietary topology and event labels |
| RSPECT | Yes | Study/image labels | No patient arterial tree | 12,195 studies | Labels too coarse for structural support |
| Augmented RSPECT | Yes | Boxes and artery names in 445 positive studies | No complete patient arterial tree | 445 positives | Multiple components; negatives empty |
| Coronary Atlas / RITE / RETA | Yes | Vessel masks/topology | Structure is the annotated target | Small | Reopens structure learning; no repeated support target |
| Sharma stream data | Yes | Occurrence and spatial data | Topologically accurate stream-network object | 537 observations | Fragmentation makes connectedness false |
| OutbreakTrees | Yes, heterogeneous | Reconstructed transmission links | Reconstructed tree is the target/estimate | 350+ outbreaks | Missing cases and structural uncertainty |

## 2. Why the fixed-tree assumption is not portable by default

The A-series exact posterior conditions on one declared tree. Across the real
candidates, that assumption has four different meanings:

| Structure status | Candidate examples | Consequence |
| --- | --- | --- |
| Fixed and known but semantically wrong for support | MeSH reduced to a tree; protein graph projected to a spanning tree | Exact inference is exact for a misspecified model |
| Fixed and known but output is trivial | Phylogenetic placement | Connectivity adds no information to a singleton |
| Instance-specific and unobserved at required resolution | Pulmonary/coronary trees | Segmentation/registration uncertainty enters before support inference |
| Operationally changing or latent | Distribution feeders; transmission trees | Conditioning on one estimated tree risks systematic overconfidence |

Therefore, “a tree can be drawn” is not evidence that the frozen DP is the
appropriate inference engine.

## 3. Empty and multi-component outcomes

A1.5's feasible decoder requires a nonempty connected output. B0 found that
empty and multi-component outcomes are common, meaningful parts of several
real targets:

- negative pulmonary-embolism studies have empty support; positive studies may
  contain bilateral or multi-lobar emboli;
- a protein may have no relevant ligand site for a requested ligand or several
  distinct interaction sites;
- a species can be absent from a watershed or fragmented across suitable
  reaches;
- multiple grid faults or switching operations can create a forest of affected
  regions;
- incomplete observation can make sampled infection cases disconnected.

Forcing a universal root, removing negative cases, or splitting one real
instance into selected connected components would change the task distribution
and often leak target information. These are not acceptable feasibility fixes.

## 4. Tractability audit

Exact inference is useful only when it solves a real computational or decision
problem. The candidates separate as follows.

### 4.1 Evidenced computational need, wrong output class

Phylogenetic placement has extreme throughput requirements and calibrated
likelihood weights, but its established algorithms optimize attachment
likelihoods over edges. The nontrivial exact computation is phylogenetic
likelihood pruning, not marginalization over connected incidence supports.

Transmission inference also needs posterior uncertainty, but integrates
epidemic, genomic, missing-case, and tree uncertainty. Exact fixed-tree support
DP does not remove the dominant uncertainty.

### 4.2 Plausible operational need, missing real data gate

Grid fault localization must be fast and interpretable for restoration. A known
radial feeder can make downstream-set reasoning tractable. However, the
available public benchmark route substitutes simulated networks or simulated
faults. Without real paired events, there is no way to establish that an exact
connected-support posterior improves the operational decision over topology
lookup, physics-based state estimation, fault indicators, or existing outage
management logic.

### 4.3 Data-rich tasks without an exact-DP bottleneck

BioASQ, protein binding, and PE detection are computationally demanding, but
their bottlenecks are representation learning, extreme label spaces, 3D image
or molecular geometry, and annotation quality. Existing task formulations do
not identify exact connected-subtree marginalization as the limiting step.

### 4.4 Spatial models whose exactness answers a different question

Stream-network ecology needs uncertainty quantification and accounts for
autocorrelation and imperfect detection. Those dependencies are not equivalent
to a prior that the occupied support is one connected subset. Exactness for the
wrong support family is not a scientific advantage.

## 5. Closest candidate: precise reopening condition

Radial-grid outage localization is the only candidate retained as a
task-level CONDITIONAL HOLD. It can be reconsidered only if one concrete data
resource supplies all of:

1. real feeder events rather than injected/simulated faults;
2. event-time observable meter/indicator measurements;
3. the event-time feeder topology and switch state;
4. line-, device-, or bus-level ground truth;
5. enough independent events for a held-out evaluation;
6. permission to publish the resulting analysis.

The target must then be audited before modeling. If common single-event labels
are empty, multi-component, or inconsistent with the topology, the hold becomes
NO-GO. No synthetic experiment is authorized while waiting for such data.

## 6. Structural uncertainty implication

If qualifying grid data eventually appears but feeder topology is estimated,
the next proposal must model or calibrate against that uncertainty. Reusing
`P(S | Y, X, \hat T)` while treating `\hat T` as error-free would be inconsistent
with the A1.5 calibration evidence. This requirement does not authorize a new
tree learner; it only prevents a known misspecification from being hidden.

## 7. Audit conclusion

The negative B0 result is driven by observed task/data mismatches, not by a
general preference against structured inference:

- public real data alone is insufficient when the support assumption is false;
- a compelling tree structure alone is insufficient when labels are synthetic
  or unavailable;
- exact computation alone is insufficient when it solves a different output
  problem.

No current dataset supports a scientifically defensible Phase B1.
