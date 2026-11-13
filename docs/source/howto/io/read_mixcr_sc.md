# Read MiXCR single-cell clone exports in R

[MiXCR](https://mixcr.com/) reconstructs and annotates immune receptor sequences. `read_mixcr()` imports [single-cell clone exports](https://mixcr.com/mixcr/reference/mixcr-export/#single-cell-libraries) containing `cellGroup`, `topChains`, and `uniqueMoleculeCount`, as in the bundled MiXCR 4.7.0 CSV example. The linked reference describes export options and fields; column names depend on the MiXCR version and export options.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain from the single-cell clone table.
- The function uses `uniqueMoleculeCount`, mapped to `umi_count`, for chain selection. `readCount` is kept separately as `consensus_count`.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

| Input field | Field in `ImmunData` |
|---|---|
| `cellGroup` | `cell_id` |
| `topChains` | `locus` |
| `allVHitsWithScore, allDHitsWithScore, allJHitsWithScore` | `v_call, d_call, j_call` |
| `nSeqCDR3` | `junction` |
| `aaSeqCDR3` | `junction_aa` |
| `uniqueMoleculeCount` | `umi_count` |
| `readCount` | `consensus_count` |

Scores in parentheses are removed from the mapped V, D, and J gene calls. The original scored fields are retained with `column_profile = "full"`.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "mixcr", "4.7.0", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_mixcr(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
