# S1.0 Dango collision and reproduction audit

## What Dango already does

Current paper: Zhang et al., *Cell Systems* 2026, DOI `10.1016/j.cels.2026.101593`. Audited repository: `ma-compbio/DANGO`, local HEAD `8104e37f8d5566b830f463b667271612ad39743a`.

| Item | Audit finding |
|---|---|
| input features | six STRING v9.1 networks: experimental, database, neighborhood, fusion, co-occurrence, co-expression; optional protein embeddings |
| architecture | per-network GNN pretraining, meta-embedding integration, modified self-attention Hyper-SAGNN regression |
| target | adjusted trigenic tau score from Kuzmin; code negates the stored score for training |
| random split | fivefold row CV (`split=0`) |
| gene split 1 | about 40--60 held genes; test contains any triple with a held gene, train contains none |
| gene split 2 | 400 held genes; test requires all three held, mixed triples discarded, train contains none held |
| classification | `|tau|>0.05` strong/weak for AUROC/AUPR; this differs from Kuzmin's `p<.05,tau<-.08` published network rule |
| regression | Pearson/Spearman overall and on strong interactions |
| uncertainty | optional variational Gaussian process on ensemble embeddings/residuals; not direct replicated-label inference |
| lower-order use | PPI networks and learned gene embeddings; not an exact tau contrast recovery from a partially observed factorial lattice |
| output | score predictions, threshold-derived classification, >400M candidate predictions; not uncertainty-aware recovery of experimentally identifiable support |

The paper reports about 91,000 mapped triples over 1,400 genes (1,395 present in PPI), replicate Pearson about 0.59, and fivefold CV. Figure 2 reports all six metric types and lower performance under both gene splits; exact bar heights are not tabulated in machine-readable text, so this audit does not invent numeric values. Gene split 1 still permits two familiar genes and familiar lower-order backgrounds; gene split 2 is stricter on identity but discards mixed triples and is still a score-prediction task.

## Reproduction status

**Not executed to metrics.** This is a concrete public-repository reproducibility failure, not a claim of insufficient compute:

1. The repository tracks `AdditionalDataS1.tsv` and six STRING adjacency files, but `Code/process.py` unconditionally requests missing `data/string_yeast_mashup_vectors_d500.txt`.
2. The same script also requests missing `data/yeast_network/yeast_genes_baker_adjacency.txt`, although README describes six networks.
3. The local environment has one RTX 4060 Laptop GPU (8 GB); the README states about 2 GB/model and defaults to eight parallel processes. A one-process run could be attempted only after reconstructing or obtaining the missing exact inputs.
4. `gpytorch` is absent locally, but that is installable and not the decisive blocker; `main.py` imports it even when GP is not requested.

No Dango source was patched and no Dango model was trained. Static code/data-path audit was sufficient to identify the blocker without manufacturing substitute embeddings.

## Residual after Dango

Dango leaves direct support recovery, experimental uncertainty/FDR, and query-background-aware evaluation incompletely addressed. However, yeast has no direct label for unmeasured triples; exploiting PPI to predict them returns to the Dango-occupied architecture/feature route. Therefore the Dango residual does not by itself establish an identifiable S1 problem.
