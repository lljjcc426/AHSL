# Phase B0 Search Log

## 1. Search date and scope

Search performed on 2026-08-26. This is a broad feasibility scoping review,
not a PRISMA systematic review or meta-analysis. It was designed to falsify or
support a specific implementation decision before any B-phase model code.

No research skill was used. Sources were located directly from publisher,
repository, government-laboratory, benchmark, and open-data pages. Technical
claims were based on primary papers or official dataset records; review papers
were used mainly to identify structural limitations and adjacent methods.

## 2. Core questions

For every task family the search asked:

1. What is the real decision or supervised target?
2. What covariates are observable at prediction time?
3. Are there repeated instances governed by a shared statistical law?
4. Is the *target support* connected on a scientifically meaningful known tree?
5. Are empty or multi-component targets common and valid?
6. Is the scaffold fixed, observed per instance, estimated, or itself latent?
7. Is exact structured inference an evidenced practical requirement?
8. Does a public real dataset jointly contain covariates, labels, and scaffold?
9. Does closer prior art already formulate the task more directly?

## 3. Search families and representative queries

### Hierarchical multilabel text

- `BioASQ biomedical semantic indexing observable title abstract MeSH labels`
- `hierarchical multilabel prediction tree DAG expected symmetric loss`
- `mandatory leaf node prediction multiple paths hierarchy`

### Protein structure and binding sites

- `BioLiP ligand binding residue database protein structure`
- `protein binding site prediction geometric graph neural network`
- `protein binding residues multiple sites structure graph`

### Phylogenetic placement

- `pplacer fixed reference tree query sequence likelihood placement`
- `EPA-ng massively parallel evolutionary placement empirical data`

### Power distribution networks

- `radial distribution outage detection smart meter fault localization`
- `real utility feeder topology smart meter outage ground truth dataset`
- `SMART-DS synthetic electrical network data`

### Vascular and pulmonary imaging

- `RSPECT pulmonary embolism artery level annotation dataset`
- `pulmonary embolism multiple bilateral emboli arterial tree`
- `coronary artery tree segmentation public dataset centerline`
- `retinal vessel topology public dataset`

### Stream-network ecology

- `fish occupancy dendritic stream network environmental covariates data`
- `fragmented fish populations stream network occurrence Dryad`
- `spatial stream network occupancy imperfect detection`

### Epidemics and diffusion

- `OutbreakTrees real transmission tree database`
- `phylogeny not transmission tree incomplete sampling`
- `diffusion source identification tree partially observed cascade`

## 4. Inclusion policy

Included evidence had to contribute at least one of:

- task definition and real evaluation;
- data composition, labels, access, or license;
- domain evidence about connectivity or fragmentation;
- scaffold availability and uncertainty;
- computational/inference requirements;
- a directly closer structured-prediction formulation.

Search snippets were not treated as evidence when a full publisher, PMC,
repository, or official dataset page was available.

## 5. Exclusion policy

The following were not accepted as a B0 pass:

- simulator-only benchmarks;
- real load profiles injected into simulated events;
- a real input dataset whose required structural labels are absent;
- papers where the tree is the prediction target rather than an observed
  scaffold;
- single-edge or single-class outputs that make connectivity trivial;
- ancestor closure or a universal root added solely to force connectivity;
- newer model papers that did not alter the data or task feasibility question.

## 6. Core sources read

### Task/data sources

1. BioASQ overview: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4450488/>
2. BioASQ CLEF 2020: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7148078/>
3. BioLiP: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3531193/>
4. pplacer: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3098090/>
5. EPA-ng: <https://academic.oup.com/sysbio/article/68/2/365/5079844>
6. SMART-DS official data record: <https://data.openei.org/submissions/2981>
7. Vector smart-meter trial: <https://doi.org/10.1049/joe.2016.0033>
8. RSPECT: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8043364/>
9. Augmented RSPECT: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10245177/>
10. RSPECT AWS record: <https://registry.opendata.aws/rsna-pulmonary-embolism-detection/>
11. Coronary Atlas: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10006074/>
12. RITE: <https://eye.medicine.uiowa.edu/rite-dataset>
13. RETA: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9273761/>
14. Himalayan trout stream data: <https://datadryad.org/dataset/doi:10.5061/dryad.f1vhhmgxh>
15. OutbreakTrees: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9255728/>

### Structural and inference sources

16. Mandatory Leaf Node Prediction: <https://proceedings.neurips.cc/paper/2012/hash/f899139df5e1059396431415e770c6dd-Abstract.html>
17. HiLAP: <https://aclanthology.org/D19-1042/>
18. ScanNet: <https://www.nature.com/articles/s41592-022-01490-7>
19. GraphBind: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8136796/>
20. Molecular source attribution: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9671344/>
21. Transmission-tree reconstruction review: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5844463/>
22. Smart-meter fault localization: <https://www.sciencedirect.com/science/article/pii/S0263224117301033>

## 7. Search stopping rule

Searching within a task family stopped when both conditions held:

1. a primary task/data source established what is actually observed and
   predicted; and
2. either a hard B0 gate failed or a qualifying real paired dataset was found.

This avoids accumulating model papers after a task-level incompatibility is
already established. The power-grid search was continued further because its
structural fit remained plausible; it stopped at the unresolved real paired
data gate.

## 8. Search result

Eight task families were evaluated. Seven are NO-GO on a core task or
structural premise. Radial-grid outage localization is a task-level
CONDITIONAL HOLD but lacks the public real paired data required for project
GO. Therefore the B0 implementation gate is NO-GO.
