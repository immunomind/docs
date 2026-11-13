# Read 10x Genomics V(D)J single-cell contigs in R

[10x Genomics Cell Ranger](https://www.10xgenomics.com/support/software/cell-ranger/latest/analysis/outputs/cr-5p-outputs-annotations-vdj) produces V(D)J contig annotations for single-cell immune profiling. `read_10x()` imports [contig annotation CSV files](https://www.10xgenomics.com/support/software/cell-ranger/latest/analysis/outputs/cr-5p-outputs-annotations-vdj) such as `filtered_contig_annotations.csv`; the linked reference describes the file layout and columns.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive contigs.
- The function uses `umis`, mapped to `umi_count`, for chain selection. `reads` is retained separately as `consensus_count`.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

| Input field | Field in `ImmunData` |
|---|---|
| `barcode` | `cell_id` |
| `contig_id` | `sequence_id` |
| `chain` | `locus` |
| `v_gene, d_gene, j_gene, c_gene` | `v_call, d_call, j_call, c_call` |
| `cdr3_nt` | `junction` |
| `cdr3` | `junction_aa` |
| `umis` | `umi_count` |
| `reads` | `consensus_count` |

Framework and non-junction CDR region amino-acid fields (`fwr1`, `cdr1`, `fwr2`, `cdr2`, `fwr3`, `fwr4`) receive an `_aa` suffix, and their `_nt` fields become the corresponding nucleotide columns. The original `cdr3` and `cdr3_nt` fields are named `source_cdr3` and `source_cdr3_nt` when retained with `column_profile = "full"`.

**Key arguments:**

- `path`: your input file or a glob matching several files. Gzip-compressed files are supported.
- `schema`: receptor features using the output column names above. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide for single-chain and paired-chain definitions.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to also keep source columns.
- `output_folder`: where to save the imported data. The example uses a temporary directory.

The example uses a small file bundled with `immunread`.

=== "R"

    ```r
    library(immunread)

    path <- system.file("extdata", "10x", "9.0.1", "contigs.csv.gz",
      package = "immunread", mustWork = TRUE)
    schema <- c("v_call", "junction_aa")

    idata <- read_10x(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )
    print(idata)
    ```
