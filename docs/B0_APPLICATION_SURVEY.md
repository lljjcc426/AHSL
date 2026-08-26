# Phase B0 Real-Task Survey

## 1. Summary matrix

`Pass` means the available evidence supports the gate. `Partial` means the
property exists only after a material reformulation or for a restricted subset
of cases. `Fail` means it conflicts with common valid outcomes or available
data.

| Candidate task | Real target and data | Observable `X` and shared law | Connected-support fit | Exact-inference need | Verdict |
| --- | --- | --- | --- | --- | --- |
| BioASQ / MeSH semantic indexing | Pass | Pass | Partial | Fail | NO-GO |
| Protein ligand/binding residues | Pass | Pass | Fail | Fail | NO-GO |
| Phylogenetic placement | Pass | Pass | Fail: usually one edge | Pass, but already task-specific | NO-GO |
| Radial-grid outage/fault localization | Partial | Pass | Partial to strong for one fixed radial event | Partial to strong | CONDITIONAL HOLD at task level; fails B0 data gate |
| Pulmonary embolus localization | Pass | Pass | Fail | Fail | NO-GO |
| Coronary/retinal vessel tasks | Partial | Pass | Fail: tree is usually the target | Fail | NO-GO |
| Fish occupancy on stream networks | Pass | Pass | Fail | Partial for other spatial models | NO-GO |
| Infection cascades / transmission | Partial | Partial | Partial only with a known complete contact tree | Partial | NO-GO |

## 2. BioASQ and hierarchical multilabel indexing

### Real mapping

- instance: a newly published biomedical article;
- observable `X_i`: title, abstract, journal, and year;
- target: MeSH descriptors assigned later by NLM curators;
- repeated population: millions of previously indexed MEDLINE articles;
- real loss: multilabel precision/recall/F measures and hierarchy-aware LCA-F.

BioASQ is an unusually strong data and covariate match. The benchmark was built
around the real delay between publication and manual MeSH indexing. Its first
release contained 10,876,004 training articles, 26,563 unique MeSH labels, and
12.55 labels per article on average. Later BioASQ editions continued the same
real online indexing setup.

Primary evidence: [BioASQ overview](https://pmc.ncbi.nlm.nih.gov/articles/PMC4450488/)
and [BioASQ at CLEF 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7148078/).

### Why it does not pass AHSL B0

MeSH is a multi-hierarchy/DAG vocabulary, and a document commonly receives
several descriptors on different branches. The released gold target is the set
of assigned descriptors, not a connected subtree on one join tree. Closing all
labels upward and adding a universal root can make any multilabel set connected,
but then connectivity becomes almost vacuous and changes the target and loss.

More importantly, hierarchical multilabel prediction with tree/DAG consistency,
multiple root-to-leaf paths, and structured posterior decisions is already a
direct literature. Mandatory Leaf Node Prediction explicitly handles tree- and
DAG-structured multilabels and optimizes structured MAP or expected symmetric
loss under a hierarchy. This is closer to BioASQ than the AHSL incidence model.

Primary evidence: [Mandatory Leaf Node Prediction](https://proceedings.neurips.cc/paper/2012/hash/f899139df5e1059396431415e770c6dd-Abstract.html)
and [Hierarchical Text Classification with Reinforced Label Assignment](https://aclanthology.org/D19-1042/).

**Decision:** real and data-rich, but the natural structured problem is
hierarchical multilabel classification, not prediction of a nonempty connected
incidence support. Exact AHSL inference is not an evidenced bottleneck.

## 3. Protein binding-site residues

### Real mapping

- instance: a protein or protein-ligand pair;
- observable `X_i`: sequence and, when available, atomic or residue-level 3D
  structure;
- target: binding residues or pockets;
- repeated population: curated protein structures and interactions.

BioLiP provides structures, biologically relevant ligands, binding residues,
affinities, and related annotations, including a downloadable non-redundant
version. This is a valid real prediction task with shared statistical structure.

Primary evidence: [BioLiP](https://pmc.ncbi.nlm.nih.gov/articles/PMC3531193/).

### Why it does not pass AHSL B0

The natural scaffold is a spatial residue/atom graph or point cloud, not a tree.
A protein may expose several pockets or interaction patches, and valid binding
residues need not form one component under an arbitrary tree projection.
Current strong methods exploit local 3D neighborhoods using geometric or graph
neural networks; ScanNet and GraphBind are direct examples.

Primary evidence: [ScanNet](https://www.nature.com/articles/s41592-022-01490-7)
and [GraphBind](https://pmc.ncbi.nlm.nih.gov/articles/PMC8136796/).

**Decision:** the target and data are real, but tree connectedness is not a
scientific property of the labels. Mapping the contact graph to a spanning tree
would discard cycles and introduce scaffold uncertainty without an exact-
inference benefit.

## 4. Phylogenetic placement

### Real mapping

- instance: a query DNA sequence or metagenomic read;
- observable `X_i`: the sequence and its alignment or derived features;
- known structure: a fixed reference phylogeny;
- target: one placement edge, or a likelihood-weight distribution over edges.

This is a real large-scale task where accurate likelihood computation and
tractability matter. EPA-ng reports placement of one billion reads onto a
3,748-taxon reference tree in under seven hours on 2,048 cores, and reports a
set of candidate branches with likelihood weight ratios.

Primary evidence: [pplacer](https://pmc.ncbi.nlm.nih.gov/articles/PMC3098090/)
and [EPA-ng](https://academic.oup.com/sysbio/article/68/2/365/5079844).

### Why it does not pass AHSL B0

The usual target for one query is a single attachment edge; a singleton is
trivially connected and contains no nontrivial subtree-support problem. A
likelihood-weight distribution over alternative edges is uncertainty over
mutually exclusive placements, not a multi-node connected label.

The computational need is genuine but is already addressed by specialized
phylogenetic likelihood pruning, preplacement, masking, and parallelization.

**Decision:** a useful negative control. It proves that “known tree + important
exact inference” is not sufficient when the output object is wrong.

## 5. Radial distribution-grid outage and fault localization

### Real mapping

- instance: a grid event;
- observable `X_i`: smart-meter last-gasp messages, voltage/current/power time
  series, remote fault indicators, switching state, and weather where available;
- scaffold: the current radial feeder topology;
- possible target: the de-energized downstream buses or the faulted line section;
- operational loss: localization accuracy and restoration latency.

Low-voltage distribution systems are commonly operated radially, and real
smart-meter trials show that meter data can help infer connectivity. Fault and
outage localization is operationally time-sensitive. For a single protective
device operation on a known, fixed radial feeder, the de-energized region can
indeed be a downstream connected subtree.

Primary evidence: [real Vector smart-meter trial](https://doi.org/10.1049/joe.2016.0033),
[fault location using smart meters](https://www.sciencedirect.com/science/article/pii/S0263224117301033),
and [distributed outage detection](https://www.osti.gov/servlets/purl/1648141).

### Blocking evidence

The public resource with detailed feeder models and time series, SMART-DS, is
explicitly synthetic. It is realistic and utility-validated, but its networks
and event labels are not real supervised events. Published studies often use a
real load profile to drive simulated IEEE or utility feeder faults, which still
does not satisfy the B0 target gate.

Primary evidence: [SMART-DS data record](https://data.openei.org/submissions/2981).

Real utility meter trials exist, but the paired feeder topology and event-level
fault/outage ground truth are generally not released as a reusable public
supervised dataset. In addition, switching, feeder reconfiguration, distributed
generation, multiple simultaneous faults, and partial observability can turn a
single fixed-tree problem into a changing-topology or multi-component problem.

**Decision:** this is the closest structural application and receives a
task-level CONDITIONAL HOLD, not a project GO. B0 fails because no qualifying
real paired dataset was identified. Simulating faults on SMART-DS would return
the project to the synthetic loop that B0 was created to stop.

## 6. Pulmonary embolus localization on the arterial tree

### Real mapping

- instance: a CTPA study;
- observable `X_i`: CT voxels and routine acquisition metadata;
- target: presence and anatomical location of pulmonary emboli;
- clinical use: triage, localization, embolic burden, and prognosis.

RSPECT contains more than 12,000 studies from five international centers. Its
augmented subset contains 445 positive studies, 30,243 bounding boxes on 14,865
images, and pulmonary-artery names from main to subsegmental branches.

Primary evidence: [original RSPECT dataset](https://pmc.ncbi.nlm.nih.gov/articles/PMC8043364/),
[AWS data record and terms](https://registry.opendata.aws/rsna-pulmonary-embolism-detection/),
and [Augmented RSPECT](https://pmc.ncbi.nlm.nih.gov/articles/PMC10245177/).

### Why it does not pass AHSL B0

One study can contain emboli in different lobes or both lungs, so the set of
affected arterial branches is commonly multi-component. Negative studies have
the empty support that the frozen nonempty decoder excludes. The augmented data
provide bounding boxes and artery names, not a complete patient-specific
pulmonary arterial tree aligned to those labels. The anatomical scaffold also
varies across patients and must be segmented or registered from the same CT.

The source paper itself frames the granular task as object detection. No
evidence was found that exact connected-subtree inference is a limiting
clinical or computational requirement.

**Decision:** excellent real imaging data, but a scientifically wrong output
constraint and a missing observed scaffold. It cannot be repaired by silently
adding a universal root or discarding bilateral/multiple emboli.

## 7. Coronary and retinal vessel tasks

Public resources contain coronary-tree segmentations/centerlines and retinal
vessel topology. These are useful for vessel segmentation and topology
recovery, but in those tasks the tree is usually the object being inferred,
not a known scaffold carrying a repeated incidence support.

Examples: [Coronary Atlas](https://pmc.ncbi.nlm.nih.gov/articles/PMC10006074/),
[RITE](https://eye.medicine.uiowa.edu/rite-dataset), and
[RETA](https://pmc.ncbi.nlm.nih.gov/articles/PMC9273761/).

Lesions can also be multiple and absent, and patient-specific trees are not in
a shared node coordinate system. Using these datasets would reopen structure
learning under a different name.

**Decision:** NO-GO under the frozen A1.5 boundary.

## 8. Fish occupancy on dendritic stream networks

### Real mapping

- instance: a species, season, or survey campaign over a stream network;
- observable `X_i`: reach geometry, water and landscape covariates, sampling
  effort, and environmental conditions;
- target: occurrence, abundance, or latent occupancy over stream reaches;
- shared law: repeated sites, dates, watersheds, or species.

The Sharma et al. Dryad release is particularly relevant: field surveys cover
218.7 km, use 537 observations, include topologically accurate spatial stream
network objects, environmental variables, and occurrence data.

Primary evidence: [Dryad dataset](https://datadryad.org/dataset/doi:10.5061/dryad.f1vhhmgxh)
and [associated Journal of Applied Ecology article](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2664.13997).

### Why it does not pass AHSL B0

The dataset and its scientific conclusion explicitly concern fragmented native
populations, mainstem displacement by invasive trout, and headwater refugia.
Habitat barriers, non-habitat reaches, recolonization, imperfect detection, and
local extinction make disconnected and empty occupancy patterns scientifically
valid. The established methodology is spatial stream-network covariance and
occupancy/abundance modeling, not a single connected-support decoder.

**Decision:** probably the strongest data-ready ecological analogue, but the
connected-support assumption contradicts the phenomenon of interest. An
empirical connectivity audit could quantify the mismatch, but it cannot make
connectivity a valid prior when fragmentation is a core biological outcome.

## 9. Infection cascades and transmission trees

### Real mapping considered

- instance: an outbreak or a partially observed cascade;
- observable `X_i`: symptom times, sampling times, locations, contacts, and
  pathogen genomes;
- possible target: infected nodes, source, or transmission links.

OutbreakTrees is an open database of more than 350 reconstructed transmission
trees from 16 directly transmitted diseases, with heterogeneous node and edge
attributes.

Primary evidence: [OutbreakTrees](https://pmc.ncbi.nlm.nih.gov/articles/PMC9255728/).

### Why it does not pass AHSL B0

The clean connected-cascade argument assumes a known, complete contact or
transmission tree and one introduction. In real outbreaks the transmission tree
is latent, cases are incompletely sampled, multiple introductions can occur,
and observed positives can be disconnected through unsampled intermediates.
Even a perfectly reconstructed pathogen phylogeny is not generally the
transmission tree because of incomplete sampling and within-host evolution.

Primary evidence: [molecular source attribution](https://pmc.ncbi.nlm.nih.gov/articles/PMC9671344/)
and [reconstruction review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5844463/).

**Decision:** uncertainty is scientifically central, but it concerns the
structure itself and missing cases. Treating a reconstructed tree as a fixed
AHSL scaffold would repeat the overconfidence mechanism identified in A1.5.

## 10. Cross-candidate conclusion

The survey exposes three distinct failure modes:

1. **Data-ready but structurally mismatched:** BioASQ, proteins, pulmonary
   emboli, and stream occupancy.
2. **Exact inference matters but the output is different:** phylogenetic
   placement and epidemic transmission reconstruction.
3. **Structurally plausible but real paired data are unavailable:** radial-grid
   outage localization.

None supports implementation of `P_theta(S_i | X_i, T)` under the frozen AHSL
output class. This is a substantive negative feasibility result, not a claim
that the underlying application areas lack important machine-learning problems.
