# Read Immcantation immune repertoire tables in R

[Immcantation](https://immcantation.readthedocs.io/en/stable/) is a toolkit for analysing adaptive immune receptor repertoires. `read_immcantation()` imports tables using its [AIRR-C format](https://changeo.readthedocs.io/en/stable/standard.html#airr-c-format) in single-cell or bulk mode. This format uses AIRR column names; the legacy Change-O format uses different names. The bundled example uses a TSV representation of the AIRR fields.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive sequences.
- In `mode = "sc"`, the function uses `umi_count` if present, otherwise `duplicate_count`, then `consensus_count`, for chain selection. The chosen column keeps its original name and meaning. At least one of these count columns is required.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.
- In `mode = "bulk"`, the function uses `duplicate_count`, otherwise `umi_count`, for abundance. With neither column, each input row represents one observed chain.

Existing AIRR names are unchanged: `cell_id`, `locus`, `v_call`, `d_call`, `j_call`, `junction`, `junction_aa`, and the count columns.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `mode`: `"sc"` for single-cell data or `"bulk"` for bulk data.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "immcantation", "single-cell.tsv.gz",package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_immcantation(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-"),
      mode = "sc"
    )
    print(idata)
    ```
