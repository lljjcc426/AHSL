# S2.0 data sources

The audit uses the temporal hypergraph collections distributed in Hypergraph
Interchange Format (HIF) by the XGI data index. Downloaded JSON files and cloned
external repositories are deliberately ignored by Git; only provenance and
derived aggregate results are versioned.

Primary collection and format documentation:

- Cornell temporal higher-order datasets: <https://www.cs.cornell.edu/~arb/data/>
- XGI data index: <https://xgi-data.github.io/>
- XGI HIF specification: <https://github.com/pszufe/HIF-standard>
- XGI Zenodo community: <https://zenodo.org/communities/xgi/>

Audited HIF files:

| Local key | File | Source family |
|---|---|---|
| email-enron | `email-enron.json` | email recipient groups |
| email-eu | `email-eu.json` | email recipient groups |
| ndc-classes | `ndc-classes.json` | drug class labels |
| ndc-substances | `ndc-substances.json` | drug substance labels |
| contact-high-school | `contact-high-school.json` | face-to-face contact groups |
| contact-primary-school | `contact-primary-school.json` | face-to-face contact groups |
| tags-ask-ubuntu | `tags-ask-ubuntu.json` | question tag sets |
| congress-bills | `congress-bills.json` | bill cosponsor sets |

`ndc-substances.json` in the current HIF release has no `edges` field. It is
recorded as `FAIL_MISSING_edges`; no timestamps or events were inferred from a
different file. The parser removes singleton events because the target is a
group event and otherwise preserves duplicate events. Dataset-specific counts
therefore refer to usable events, not necessarily the raw source totals.

License metadata is inherited from each XGI/Zenodo record; the inspected
collection records declare CC BY 4.0. Reusers should cite the individual Zenodo
record in addition to the original dataset publication.
