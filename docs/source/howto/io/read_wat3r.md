# Read WAT3R single-cell TCR tables in R

[WAT3R](https://github.com/mainciburu/WAT3R) associates T-cell receptor sequences with 3′ single-cell RNA sequencing data. `read_wat3r()` imports its [barcode_results.csv output](https://github.com/mainciburu/WAT3R#downstream) with `BC`, TRA, TRB, and optional secondary TRA columns, as shown below. The [WAT3R paper](https://doi.org/10.1093/bioinformatics/btac382) describes the workflow and its barcode-linked TCR output.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain. It splits paired TRA/TRB input rows into separate chain rows and includes any supplied secondary TRA (`TRA.2`) chains before receptor selection. It removes empty chain entries.
- The function uses `TRA_CDR3_UMIcount`, `TRB_CDR3_UMIcount`, or `TRA.2_CDR3_UMIcount` for the corresponding chain, mapped to `umi_count`. Every supplied chain group needs its count column.
- The reader maps each chain’s `*_nReads` value to `consensus_count`. Set `column_profile = "full"` to also retain the original wide-format read-count columns. Chain selection uses `umi_count`.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

| Input field | Field in `ImmunData` |
|---|---|
| `BC` | `cell_id` |
| `TRAV, TRBV, TRAV.2` | `v_call` |
| `TRBD (TRB only)` | `d_call` |
| `TRAJ, TRBJ, TRAJ.2` | `j_call` |
| `TRA_CDR3nuc, TRB_CDR3nuc, TRA.2_CDR3nuc` | `cdr3` |
| `TRA_CDR3, TRB_CDR3, TRA.2_CDR3` | `junction_aa` |
| `TRA_CDR3_UMIcount, TRB_CDR3_UMIcount, TRA.2_CDR3_UMIcount` | `umi_count` |
| `TRA or TRB from the column group` | `locus` |

Secondary TRA columns use the `TRA` locus. You can keep the source read-count columns by setting `column_profile = "full"`, although the function does not use them to select chains.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "wat3r", "1.3", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- immundata::make_receptor_schema(
      features = c("v_call", "junction_aa"),
      chains = c("TRA", "TRB")
    )

    idata <- read_wat3r(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
