# Glossary

## Cell & Molecular Immunology

**TCR / BCR** *(noun)*
Protein complexes forming the **T‑cell receptor** (TCR) and **B‑cell receptor** (BCR). They recognise antigens via specific binding sites and drive downstream immune signalling. In repertoire data, TCR usually refers to TRA/TRB chains; BCR to IGH/IGK/IGL.

**Chain** *(noun)*
One polypeptide chain that is part of a receptor, for example **TRA**, **TRB**, **IGH**, **IGK**, **IGL**. Chains pair to form the full receptor (e.g., TRA+TRB; IGH+IGK/IGL). “Chain” is not the same as *locus* (genomic location).

**V(D)J recombination** *(noun)*
Somatic DNA rearrangement in developing lymphocytes that joins **V**, (optionally **D**), and **J** gene segments to generate receptor diversity.

**CDR3 (AA/NT)** *(noun)*
**Complementarity‑determining region 3**, represented as amino‑acid (`cdr3_aa`) or nucleotide (`cdr3_nt`) sequence. CDR3 spans the V‑D‑J junction and often determines antigen specificity; it is central to clonotype definitions.

**V / J / D gene** *(noun)*
Germline gene segments that contribute to the variable region of TCR/BCR. In data tables these appear as calls such as `v_call`, `j_call`, `d_call` (possibly with allele information).

**Isotype / Class** *(noun)*
For immunoglobulins (BCR heavy chain) the constant‑region class: **IgM**, **IgD**, **IgG**, **IgA**, **IgE**. Isotype affects effector function and tissue distribution. Not applicable to TCRs.

**Somatic hypermutation (SHM)** *(noun)*
Point mutations introduced into the Ig variable region after antigen exposure, typically in germinal centres. SHM refines affinity during B‑cell maturation; it is not observed in TCRs.

**Class‑switch recombination (CSR)** *(noun)*
DNA recombination in B cells that changes the immunoglobulin heavy‑chain **class** (e.g., IgM→IgG) **without altering antigen specificity**.

**Epitope** *(noun)*
A specific part of an antigen recognised by a receptor or antibody. Epitopes may be linear (sequence) or conformational (structure‑dependent).

**Antigen specificity** *(noun)*
Evidence that a receptor recognises a particular epitope or antigen; may be experimentally validated or inferred. **State the evidence type when reporting.**


## AIRR Data Model & Schemas

**Receptor** *(noun)*
A unique **receptor observation (record)** in the dataset, represented by one chain pair (e.g., TRA+TRB or IGH+IGK/IGL) or a single chain when pairs are unavailable. Field: `imd_receptor_id`.

**Clonotype** *(noun)*
A **group of receptors** defined by an explicit rule, commonly identical **CDR3 amino‑acid** sequence together with the same **V/J** genes. Other rules exist (e.g., nucleotide‑level identity or distance‑based clustering); always state the rule used.

**Clone** *(noun; potentially ambiguous)*
Often used informally for *clonotype* or for a population of cells sharing a clonotype. Prefer *clonotype* unless a biological cell clone is intended; define your usage once per document.

**Repertoire** *(noun)*
All receptors for a **biological or analysis unit** (e.g., sample, subject, tissue, timepoint, therapy group). Repertoires are the natural level for counts, proportions, clonality and diversity. Field: `imd_repertoire`.

**Sample / Subject / Timepoint** *(nouns)*
Common metadata levels. *Sample* is a processed specimen; *subject* is the individual or organism; *timepoint* is the collection time or study visit. Define your usage explicitly in Methods.

**Barcode** *(noun)*
A single‑cell identifier used to link receptor data to transcriptomic data (Seurat/AnnData). Barcodes are case‑sensitive and must match the cell IDs in the external object. Field: `imd_barcode`.

**Contig** *(noun)*
An assembled VDJ sequence record reported by VDJ callers (e.g., 10x Genomics V(D)J). **Contigs can be productive or non‑productive and may include quality metrics.**

**Productive** *(adjective)*
Indicates that a contig or receptor is in‑frame and lacks a premature stop codon, yielding a potentially functional protein.

**Count** *(noun)*
The observed abundance of a receptor within a repertoire, often derived from UMI‑collapsed reads. Counts are **per repertoire** (the same receptor may have different counts in different repertoires). Field: `imd_count`.

**Proportion** *(noun)*
Per‑repertoire **normalised abundance** (each repertoire sums to **1**). Field: `imd_proportion`.

**Receptor ID** *(noun)*
A unique identifier used to join tables (e.g., linking annotations to counts). May be a hash of key sequence fields or an explicit ID column.

**AIRR format** *(noun)*
The community standard for AIRR data representation and metadata. Field names and semantics are defined by the AIRR Community; using the standard improves tool interoperability.

**Schema** *(noun)*
A mapping that tells `ImmunData` which columns in the annotations represent the receptor, repertoire, barcode, and other key fields (e.g., `schema_receptor`). Schemas make code portable across datasets with different column names.

**Aggregation / `agg_repertoires()`** *(noun/verb)*
The process of building repertoire‑level tables from receptor annotations using a chosen grouping (sample, tissue, etc.). Aggregation locks the analysis unit so that counts and proportions are well defined.

**Snapshot / Immutability** *(noun)*
Saving the **current state** of an `ImmunData` object to disk after expensive steps (e.g., annotations). Snapshots avoid repeating prior work, improve reproducibility, and speed up iteration.


## Analytics & Metrics

**Gene usage** *(noun)*
The frequency distribution of V, J and (where applicable) D gene calls within a repertoire or cohort. Often used to compare immunological states or technical batches.

**Clonality** *(noun)*
The degree to which a repertoire is dominated by a small number of receptors. In `immunarch`, clonality can be summarised by **proportion bins** (e.g., Hyperexpanded, Large, …) or by **rank bins** (e.g., top‑10, top‑100). Both views highlight overabundance, but from different angles.

**Rank‑abundance line** *(noun)*
Curve within a repertoire that orders receptors by abundance (count or proportion) and plots **abundance vs rank** to show dominance and tail behaviour.

**D50 / DXX** *(noun)*
The minimal number of top receptors required to accumulate **X%** of a repertoire’s total abundance (e.g., **D50** for 50%). Lower values indicate stronger dominance by high‑abundance receptors.

**Diversity indices** *(noun)*
Quantitative measures of repertoire diversity, such as **Shannon** entropy, **Simpson** index, and **Hill numbers**. Each index emphasises richness vs evenness differently; specify the index and base when reporting.

**Evenness (Pielou)** *(noun)*
A normalised measure of how evenly abundance is distributed among receptors, derived from Shannon entropy. High evenness means similar abundances; low evenness indicates dominance.

**Overlap** *(noun)*
Similarity between repertoires (e.g., **Jaccard**, **Morisita–Horn**). **Always state the matching rule** (e.g., clonotype definition) and the index used.

**Public clonotype / Publicity** *(noun)*
A clonotype observed in multiple individuals. Publicity can be defined by simple presence across subjects or by quantitative measures (e.g., Jaccard across repertoires). Define the criterion used.

**Convergent recombination (Convergence)** *(noun)*
Independent nucleotide sequences that encode the **same amino‑acid** receptor sequence (often the same CDR3 AA), suggesting selection or recombination bias.

**Motif** *(noun)*
A recurring sequence pattern, such as a **k‑mer**, regular expression, or GLIPH‑like motif, that may correlate with specificity or structure.

**Convergence score** *(noun)*
Numeric measure of sequence‑level convergence **(methods vary; report the definition with the score)**.


## Workflows & Visualisation

**QC / Filtering** *(noun)*
Initial checks and thresholds applied before analysis (e.g., removing non‑productive contigs, extreme lengths, low‑quality calls). Good QC prevents bias downstream.

**Normalisation** *(noun)*
Scaling within each repertoire so that abundances are comparable (e.g., converting counts to proportions). Always state the rule used and whether additional scaling was applied.

**Subsampling / Rarefaction** *(noun)*
Downsampling to a common depth for fair comparisons; **report the target depth and random seed** when relevant.

**UMAP / t‑SNE / PCA** *(noun)*
Dimensionality‑reduction methods used to embed high‑dimensional features (e.g., sequence embeddings) for visualisation. Choice of method and parameters can affect apparent structure.

**Feature table** *(noun)*
A tabular matrix of engineered features for ML/DL (e.g., V/J one‑hots, k‑mer counts, CDR3 embeddings). Feature tables can be exported to Parquet for cross‑language training.

**Embedding** *(noun)*
A continuous vector representation of sequences or cells (e.g., CDR3 embedding) used for similarity search, clustering, or downstream prediction.


## Tooling & Infrastructure

**ImmunData** *(proper noun)*
An R6 data container that stores receptor‑level annotations and repertoire‑level summaries using schemas aligned with AIRR. It supports lazy operations, rapid aggregation, and snapshotting.

**`annotate_*`** *(family)*
Functions that add columns to `ImmunData` (e.g., clonality labels, meta‑annotations). They preserve the original data and extend it with new fields.

**`airr_*`** *(family)*
Functions that compute repertoire‑level statistics and summaries (e.g., clonality, diversity, overlap) from an `ImmunData` object.

**`receptor_*`** *(family)*
Functions that filter or transform receptors (rows) within `ImmunData` (e.g., select chains, length ranges, or productivity).

**`annotate_seurat()`** *(function)*
A helper that copies selected columns from `ImmunData` to a Seurat object using **`barcode`** as the join key, enabling UMAP colouring by receptor labels.

**Arrow / Parquet** *(proper nouns)*
Columnar storage formats used on disk. They support efficient compression, fast column access, and interoperability across languages.

**DuckDB / duckplyr / dbplyr** *(proper nouns)*
An embedded analytical database (**DuckDB**) and R packages that translate tidy verbs to SQL (`duckplyr`, `dbplyr`). They enable lazy execution and scale beyond RAM.

**Lazy evaluation** *(noun)*
A computation model where operations are recorded but not executed until needed. It reduces memory pressure and allows the backend to optimise query plans.

**Materialise / `compute()` / `collect()`** *(verbs/functions)*
*Materialise* means persist results. `compute()` creates a (temporary) table inside DuckDB; `collect()` pulls the result into R memory as a data frame.

**Registry** *(noun)*
A mechanism in `immunarch` for registering method implementations so families like `airr_*` can expose multiple named strategies under one interface.