# Read Parse Biosciences single-cell TCR tables in R

[Parse Biosciences Evercode TCR](https://www.parsebiosciences.com/products/evercode-tcr/) measures T-cell receptors in single cells. `read_parsebio()` imports TCR CSV tables containing separate TRA and TRB column groups.

See Parse's [pipeline output guide](https://support.parsebiosciences.com/hc/en-us/articles/36215329630228-Guided-walkthrough-Pipeline-Outputs) for output files and links to detailed customer documentation. This reader expects the wide layout shown below, with `Barcode`, `TRA_*`, `TRB_*`, and optional `secondary_TRA_*` / `secondary_TRB_*` columns. For [AIRR-formatted `tcr_annotation_airr.tsv` exports](https://support.parsebiosciences.com/hc/en-us/articles/36453291031700-Generating-Full-TCR-Alpha-and-Beta-Sequences-with-stitchr), use [`read_airr_sc()`](read_airr_sc.md).

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain. It splits paired TRA/TRB input rows into separate chain rows and includes any supplied `secondary_TRA` and `secondary_TRB` chains before receptor selection. It removes empty chain entries.
- The function uses each chain's `<prefix>_transcript_count`, mapped to `umi_count`, for chain selection. A count is required for every supplied chain group.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

| Input field | Field in `ImmunData` |
|---|---|
| `Barcode` | `cell_id` |
| `<prefix>_V, <prefix>_D, <prefix>_J, <prefix>_C` | `v_call, d_call, j_call, c_call` |
| `<prefix>_cdr3_aa` | `junction_aa` |
| `<prefix>_transcript_count` | `umi_count` |
| `TRA or TRB from the column prefix` | `locus` |

Here, `<prefix>` is `TRA`, `TRB`, `secondary_TRA`, or `secondary_TRB`. Secondary prefixes map to the same `TRA` or `TRB` locus. You can keep the source read-count columns by setting `column_profile = "full"`, although the function does not use them to select chains.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "parsebio", "1.6.1", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- immundata::make_receptor_schema(
      features = c("v_call", "junction_aa"),
      chains = c("TRA", "TRB")
    )

    idata <- read_parsebio(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
