# N1.0 Reactome data freeze

Freeze date: 2026-08-26 (Asia/Shanghai). The official download page states that quarterly Zenodo snapshots are available beginning with V89; Reactome data and derived files are CC0.

| Role | Release | Release date | BioPAX artifact | Bytes | SHA-256 | Downloaded |
|---|---:|---|---|---:|---|---|
| historical | V89 | 2024-06 | `https://download.reactome.org/89/biopax.zip` | 160,613,110 | `1570AB7BC3DFEE26CBEC9A841F49B88131D808797ED4426B026C67CA6FA8E94B` | 2026-08-26 23:16 CST |
| later temporal snapshot | V97 | 2026-06-30 | `https://reactome.org/download/current/biopax.zip` (current V97 at freeze time; versioned directory `https://download.reactome.org/97/`) | 173,989,993 | `EFEDB0F6BD9FB788056D9F8AC1D5916B5EFC25FBCD03606C618A051C46E7A4D7` | 2026-08-26 23:21 CST |

Both archives contain BioPAX Level 3 OWL. The parsed files were `Homo_sapiens.owl` (V89: 306,800,355 bytes; V97: 333,253,965 bytes). Raw archives, extracted data, parser caches, and external inspection clones are excluded from Git; the checksums above are the single integrity record required by the protocol.

The V89 HTTP metadata reported `Last-Modified: Tue, 11 Jun 2024 14:07:38 GMT`; the V97 archive reported `Last-Modified: Wed, 24 Jun 2026 19:18:48 GMT`. The release calendar identifies V97 as the June 30, 2026 release. Data licensing source: `https://reactome.org/license`; download inventory: `https://reactome.org/download-data`.

Historical isolation rule: a V89 task may use only V89 graph incidence, entity state/compartment, reaction type, and V89 pathway hierarchy. V97 was used only to classify later tasks as NEW, MODIFIED, or UNCHANGED. No V97 annotation was joined into V89 features.

The freeze intentionally uses two releases, not a fabricated middle calibration release: N1.0 performs no model fitting or calibration. If a later ML phase had been authorized, a calibration release would have needed a new predeclared freeze.
