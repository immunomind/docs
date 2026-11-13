# Read Dandelion single-cell immune receptor contigs in R

[Dandelion](https://sc-dandelion.readthedocs.io/en/latest/) analyses single-cell B-cell and T-cell receptor data. `read_dandelion()` imports its [AIRR contig table](https://sc-dandelion.readthedocs.io/en/latest/notebooks/base/0_dandelion_primer.html), corresponding to the `Dandelion.data` structure rather than the per-cell `metadata` table. The bundled example uses a CSV representation of the contig table.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive contigs.
- The function uses `umi_count` for chain selection when present. Otherwise, it renames `duplicate_count` to `umi_count` and uses that. If neither is present, it uses `consensus_count`. When `duplicate_count` is renamed, its original value is also retained as `source_duplicate_count` if `column_profile = "full"` is passed.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

Existing AIRR names such as `cell_id`, `locus`, `v_call`, `d_call`, `j_call`, `junction`, `junction_aa`, and `consensus_count` are unchanged.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "dandelion", "0.5.5", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_dandelion(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
