# S1.0 yeast audit

## Source and exact public table

Primary source: Kuzmin et al., *Science* 2018, DOI `10.1126/science.aao1729`; data accession `10.5061/dryad.tt367`. The downloaded `AdditionalDataS1.tsv` has 501,510 rows: 410,399 digenic and 91,111 trigenic rows. There are 91,050 unique unordered triples, 1,400 unique genes, 182 double-mutant query pairs, 359 query genes, and 1,180 array genes.

The paper reports testing 195,666 triple mutants, but this is not the same quantity as usable aggregate trigenic rows in S1. The experimental program used 182 double-query strains, 364 single-query controls, a diagnostic array of roughly 1,200 genes, at least two replicate screens, and matching digenic screens. The protocol generates multiple colonies per genotype; public S1 is an aggregate table, not raw colony replicates.

## Estimand and uncertainty

Tau-SGA subtracts scaled digenic contributions from raw trigenic epsilon. The accepted negative rule `p<0.05 and tau<-0.08` yields exactly 3,196 labels; there are no strong positive labels under the symmetric positive rule because public tau ranges from -1.0816 to 0. The remaining 87,915 rows are `UNCERTAIN_OR_NULL`, not certain negatives.

The combined-mutant fitness SD has median 0.0564. Kuzmin reports validation around the CLN1--CLN2 query with roughly 40% false negatives, 20% false positives, and 60--75% true positives. Dango reports replicate-score Pearson near 0.59 for trigenic versus 0.88 for digenic data. Consequently the scientifically preferable target is latent trigenic status under repeated noisy measurement; the published threshold is a usable but noisy operational label.

Raw epsilon versus adjusted tau gives support Jaccard 0.505 and rank Spearman 0.267. This does not make tau arbitrary: it shows that removing lower-order effects materially changes the structure, exactly as tau is designed to do.

## Missingness and identifiability

- A measured triple with its matching lower-order screen information is `IDENTIFIABLE_WITH_NOISE`.
- An unmeasured triple is `NOT_IDENTIFIABLE` from the experimental table alone. PPI, embeddings, or shared-gene patterns can support prediction, but then truth is supplied only when that triple is experimentally measured.
- Triple rows sharing query pairs, genes, plates, and neighborhoods are dependent. Row count is not iid sample size.
- Order extrapolation from digenic to trigenic *score prediction* requires an explicit transfer model; digenic scores alone do not identify arbitrary tau support.

## Validation consequence

Random row split is diagnostic only. Query-pair-disjoint evaluation retains 72,964 train and 18,147 test rows, with zero shared query pairs but 100% any-gene overlap and 4.14% any-pair overlap. Gene-disjoint-any-held is not “all genes unseen”: 90.2% of test triples still contain at least one train gene. Batch-level leakage cannot be fully audited because raw plate/batch identifiers are not in public S1.
