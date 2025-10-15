# `ImmunData` schema

This page defines the **internal tables and standard column names** used inside an `ImmunData` object. These names are stable across functions in `immundata` and packages, which depend on it, such as `immunarch`.

Important: You rarely need to touch internal tables directly. Treat them as managed by `immundata`. Direct edits can break referential integrity and invalidate results. Prefer high-level functions and accessors, supplied by packages.

The column names can be accessed or retrieved programmatically via their names directly, e.g., `imd_<key>`, or via aliases `immundata::imd_schema("<key>")`. 

## Core tables

* **Annotations** (`idata$annotations`): the physical, barcode-level table that stores chain/rearrangement records plus per-barcode (cell/spot) metadata. One or more chains may belong to the same barcode. Stored on the disk in Parquet files and in DuckDB.
* **Receptors** (`idata$receptors`): a **virtual** (computed) view that returns receptor-level rows according to the active receptor schema (e.g., single chain, αβ TCR, heavy+light BCR). Each receptor keeps links back to its source barcode(s)/chain(s). 
* **Repertoires** (`idata$repertoires`): a physical table with repertoire IDs and basic counts created by `agg_repertoires()` (e.g., group by sample, donor, condition). `idata$metadata` uses this table to show the sample-level information.

Hierarchically, **chains → barcodes → receptors → repertoires** are the building blocks. `immundata` keeps full lineage between them. 

## Canonical column names

> **Reminder:** use canonical column names such as `imd_count` in exploratory scripts and notebooks. Use keys with `imd_schema()` for packages.

These are the standardized names `imd_schema()` returns and that functions expect across the stack.

| Key (for `imd_schema()`)       | Canonical column    | Core table              | Meaning                                                      |
| ------------------------------ | ------------------- | ----------------------- | ------------------------------------------------------------ |
| `"receptor"`                   | `imd_receptor_id`   | receptors/annotations   | Stable receptor identifier.                                  |
| `"barcode"` / `"cell"`         | `imd_barcode`       | annotations             | Barcode (cell/spot) identifier.                              |
| `"chain"`                      | `imd_chain_id`      | annotations             | Unique chain/rearrangement identifier.                       |
| `"repertoire"`                 | `imd_repertoire_id` | repertoires/annotations | Repertoire (group) identifier.                               |
| `"count"` / `"receptor_count"` | `imd_count`         | receptors/repertoires   | Count of receptors per group (semantics depend on context).  |
| `"chain_count"`                | `imd_n_chains`      | annotations/receptors   | Number of chains contributing to a receptor/barcode.         |
| `"proportion"`                 | `imd_proportion`    | annotations             | Proportions derived from counts.                             |
| `"n_receptors"`                | `n_receptors`       | repertoires             | Total receptors in a repertoire.                             |
| `"n_barcodes"`                 | `n_barcodes`        | repertoires             | Total barcodes in a repertoire.                              |
| `"n_cells"`                    | `n_cells`           | repertoires             | Alias for barcodes when they represent cells.                |
| `"n_repertoires"`              | `n_repertoires`     | repertoires             | Count of repertoires (e.g., cohort level).                   |
| `"locus"`                      | `locus`             | annotations             | Chain locus (e.g., TRA, TRB, IGH, IGL).                      |
| `"metadata_filename"`          | `imd_filename`      | annotations             | Source filename used during ingest.                          |
| `"filename"`                   | `filename`          | annotations             | User-facing filename column (if present).                    |

**Similarity flags (prefixes):** columns created by similarity/matching utilities may use the following **prefixes**; the suffix is method-specific (e.g., the field compared).
`imd_sim_exact_`, `imd_sim_regex_`, `imd_sim_hamm_`, `imd_sim_lev_`. 

## Feature columns used to *define* receptors

Your receptor schema declares which **features** identify a receptor (e.g., *CDR3 AA*, *V gene*, optionally *J gene*), and which **chains** to pair (e.g., α+β). `Receptors` are computed on the fly from `annotations` using that schema. 

* Typical gene/sequence fields align to **AIRR-C** conventions and are normalised on ingest. E.g., **10x Genomics** columns are renamed: `v_gene → v_call`, `j_gene → j_call`
* Common feature columns then are: `v_call`, `j_call`, and a CDR3 field (often `junction_aa`/`cdr3`/`cdr3_aa`, depending on your source). Choose the exact set when you build the receptor schema. 

## Accessing names programmatically

### Direct (scripts)

=== "R"

    ```r
    library(immunarch)

    idata |> 
        filter(imd_count >= 5)
    ```

### Schema-resolved (packages)

=== "R"

    ```r
    library(immunarch)

    cnt <- immundata::imd_schema("count")
    idata |> 
        filter(!!rlang::sym(cnt) >= 5)

    # imd_schema_sym("<key>") == rlang::sym(imd_schema("<key>"))
    cnt_sym <- immundata::imd_schema_sym("count")
    idata |> 
        filter(!!cnt_sym >= 5)

    imd_schema("barcode")     # "imd_barcode"
    imd_schema("receptor")    # "imd_receptor_id"
    imd_schema("repertoire")  # "imd_repertoire_id"
    ```

These helpers are used internally across immunarch methods for safe joins and checks. 

## Common pitfalls when loading data (and why)

* **No repertoires defined**: many analyses expect `imd_repertoire_id`. Create it with `agg_repertoires()` (e.g., group by `sample_id`, `donor`, `timepoint`). 
* **Ambiguous receptor schemas**: for multi-chain receptors (αβ, heavy+light), specify pairing rules (which loci to pair, tie-breakers for multiple chains per barcode). 