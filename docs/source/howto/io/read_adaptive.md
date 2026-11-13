# Read Adaptive immunoSEQ Analyzer and Connector bulk tables in R

[Adaptive Biotechnologies](https://www.adaptivebiotech.com/our-platform/) provides immune repertoire sequencing. `read_adaptive()` imports bulk immunoSEQ Analyzer, Analyzer v2, and Connector TSV exports.

See Adaptive's [Analyzer TSV export guide](https://www.adaptivebiotech.com/wp-content/uploads/2019/07/MRK-00342_immunoSEQ_TechNote_DataExport_WEB_REV.pdf) for rearrangement-level column definitions, and the legacy [Analyzer manual, Sample Export section](https://clients.adaptivebiotech.com/assets/downloads/immunoSEQ_AnalyzerManual.pdf) for the older column layout.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function keeps sequences marked as in-frame (`In`) and returns an `ImmunData` object with one row per retained chain.
- The function uses `templates` for Analyzer and Connector abundance, and `count (templates/reads)` for Analyzer v2. The function maps the selected column to `duplicate_count` to store the abundance of each chain.

| Input field | Field in `ImmunData` |
|---|---|
| `v_resolved, d_resolved, j_resolved` | `v_call, d_call, j_call` |
| `cdr3_rearrangement (Analyzer) or cdr3_nucleotide (Connector)` | `junction` |
| `cdr3_amino_acid` | `junction_aa` |
| `templates` | `duplicate_count` |
| `vMaxResolved, dMaxResolved, jMaxResolved (Analyzer v2)` | `v_call, d_call, j_call` |
| `aminoAcid (Analyzer v2)` | `junction_aa` |
| `nucleotide (Analyzer v2)` | `sequence` |
| `count (templates/reads) (Analyzer v2)` | `duplicate_count` |
| `frame_type or sequenceStatus equals In` | `productive` |

Analyzer v2's `nucleotide` contains a full sequence, so the function stores it as `sequence` rather than extracting a CDR3 `junction`. `seq_reads` remains a separate source field when retained with `column_profile = "full"`.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "adaptive", "analyzer", "contigs.tsv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_adaptive(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
