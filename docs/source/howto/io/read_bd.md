# Read BD Rhapsody single-cell immune repertoire contigs in R

[BD Rhapsody](https://www.bdbiosciences.com/en-us/products/reagents/single-cell-multiomics/bd-rhapsody-tcr-bcr-next-multiomic-assays) profiles T-cell and B-cell receptors alongside single-cell measurements. `read_bd()` imports its [VDJ Contigs AIRR tables](https://bd-rhapsody-bioinfo-docs.genomics.bd.com/outputs/outputs_vdj_contigs.html). The linked reference lists the output files and defines cell identifiers, receptor annotations, and read and molecule counts; the bundled example uses a CSV representation of these fields.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive contigs.
- The function uses `umi_count` for chain selection when present. Otherwise, it renames `duplicate_count` to `umi_count` and uses that. If neither is present, it uses `consensus_count`. When `duplicate_count` is renamed, its original value is also retained as `source_duplicate_count` if `column_profile = "full"` is passed.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

The input already uses AIRR names such as `cell_id`, `locus`, `v_call`, `d_call`, `j_call`, `junction`, `junction_aa`, and `consensus_count`. These names are unchanged.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "bd", "2.3", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_bd(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
