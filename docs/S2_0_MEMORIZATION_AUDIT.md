# S2.0 Memorization Audit

## Threat model

The no-learning memorization family ranks exact historical sets by total
frequency or most recent occurrence. It can only retrieve a novel set if the
evaluation candidate construction has already leaked or supplied it, so its
novel-set exact recall is correctly zero.

| Dataset | test repeat rate | best frequency Hit@1 / Recall@10 | recency Hit@1 / Recall@10 | novel frequency Recall@1 / @10 |
|---|---:|---:|---:|---:|
| tags-ask-ubuntu | 40.57% | 0.207% / 1.330% | 0.018% / 0.110% | 0 / 0 |
| congress-bills | 18.84% | 0.461% / 0.577% | 0 / 0.010% | 0 / 0 |

Frequency is the strongest aggregate local baseline because repeated sets are
present, but it does not dominate the scientifically meaningful novel-set
subset. Therefore the strict “all usable datasets >=80% repeats and recurrence
captures most performance” kill rule does not fire: Ubuntu and Congress are
well below 80%.

The other datasets explain why aggregate AUC or aggregate recall is dangerous:
high school 97.04%, primary school 93.80%, Email-EU 91.25%, Enron 87.18%, and
NDC classes 98.50% of sequential test events are exact repeats. A method can
appear strong there by learning event identity frequency or recency, without
forming a new group. Published aggregate results cannot be decomposed unless
their evaluation releases event-level predictions; we therefore state this as
a plausible mechanism, not a re-estimated claim about a particular paper.

The residual after memorization is real in sample count (19,530 and 15,477
novel events), but local exact retrieval remains at zero Recall@10 because the
candidate/search stage misses nearly every novel truth.
