# Read TRUST4 single-cell immune receptor tables in R

[TRUST4](https://github.com/liulab-dfci/TRUST4) reconstructs T-cell and B-cell receptors from RNA sequencing data. `read_trust4()` imports cell-level CSV tables with embedded primary and secondary chain records. The [barcode report format documentation](https://github.com/liulab-dfci/TRUST4#10x-genomics-data-and-barcode-based-single-cell-data) defines the comma-separated fields inside each chain record; the bundled example uses `X.barcode`, `chain1`, `chain2`, `secondary_chain1`, and `secondary_chain2` as table headers. The [TRUST4 paper](https://doi.org/10.1038/s41592-021-01142-2) describes the reconstruction workflow.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain. It expands records from `chain1`, `chain2`, `secondary_chain1`, and `secondary_chain2` into separate chain rows, including secondary records separated by semicolons. It removes empty records.
- The reader floors the embedded `read_cnt` estimate to create `consensus_count`, which it uses for chain selection. Set `column_profile = "full"` to retain the original estimate as `source_read_count`.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

| Input field | Field in `ImmunData` |
|---|---|
| `X.barcode` | `cell_id` |
| `Chain record fields 1–4: V, D, J, C genes` | `v_call, d_call, j_call, c_call` |
| `Chain record field 5: nucleotide CDR3` | `junction` |
| `Chain record field 6: amino-acid CDR3` | `junction_aa` |
| `Chain record field 7: read_cnt` | `consensus_count` |
| `Chain record field 8: contig ID` | `sequence_id` |
| `Gene locus from the V call, or J call when V is missing` | `locus` |

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "trust4", "1.1.7", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_trust4(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
