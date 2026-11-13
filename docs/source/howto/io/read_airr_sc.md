# Load single-cell sequencing immune repertoire data in AIRR-C format to `immunarch` in R

The [AIRR Rearrangement format](https://docs.airr-community.org/en/stable/datarep/rearrangements.html) stores immune receptor sequences and annotations in TSV files. `read_airr_sc()` imports single-cell AIRR data with cell barcodes, loci, and UMI or read counts.

The specification documents the [TSV input structure](https://docs.airr-community.org/en/stable/datarep/rearrangements.html#file-format-specification) and the meaning of each annotation field, including `cell_id` and `locus`.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive contigs.
- The function uses `umi_count` if present, otherwise `duplicate_count`, then `consensus_count`, for chain selection. At least one of these columns is required, and each keeps its original meaning.
- If you request paired receptors, the function selects the chain with the highest count at each required locus for each barcode. It keeps only cells with both required chains.

AIRR names such as `cell_id`, `locus`, `v_call`, `d_call`, `j_call`, `junction`, and `junction_aa` are unchanged. If `cell_id` is absent, `barcode` is copied to `cell_id`. Count columns are not renamed.

## Quick start with immunread

**Key arguments:**

- `path`: the input file or a glob matching several files.
- `schema`: receptor features using AIRR column names and the loci to analyse. See the [receptor schema](../../guides/schemas/receptor_schema.md) guide.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to keep all source columns.
- `output_folder`: where to store the imported data. The example uses a temporary directory.

=== "R"

    ```r
    library(immunread)

    path <- system.file(
      "extdata", "airr", "2.0-sc", "contigs.tsv.gz",
      package = "immunread", mustWork = TRUE
    )
    schema <- immundata::make_receptor_schema(
      features = c("v_call", "junction_aa"),
      chains = "TRB"
    )
    # This fixture contains TRB only. For your paired TRA/TRB data,
    # use chains = c("TRA", "TRB").

    idata <- read_airr_sc(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )

    print(idata)
    ```

Replace `path` with your own file or a glob such as `"/path/to/sc_airr/*.tsv"`. Choose a permanent `output_folder` when you want to keep the imported data.

## Advanced: read_repertoires()

Use `immundata::read_repertoires()` directly when you want to choose the input columns and preprocessing yourself. This is also the reader used by `immunread`.

**Key arguments:**

- `path`: your input file or glob, or `"<manifest>"` to read files listed in a manifest.
- `schema`: the receptor features and loci to analyse.
- `barcode_col`: the cell identifier column, usually `"cell_id"`.
- `locus_col`: the chain locus column, usually `"locus"`.
- `umi_col`: the UMI/read-count column used to select chains, such as `"umi_count"` or `"duplicate_count"`. A count column is required.
- `preprocess`: transformations applied before receptor construction.
- `manifest`: an optional table of file paths and sample information.
- `repertoire_schema`: columns that define your repertoires, such as patient or tissue.

This example uses the same bundled file and sets the column names explicitly.

=== "R"

    ```r
    library(immundata)

    path <- system.file(
      "extdata", "airr", "2.0-sc", "contigs.tsv.gz",
      package = "immunread", mustWork = TRUE
    )
    schema <- immundata::make_receptor_schema(
      features = c("v_call", "junction_aa"),
      chains = "TRB"
    )
    # This fixture contains TRB only. For your paired TRA/TRB data,
    # use chains = c("TRA", "TRB").

    idata <- read_repertoires(
      path = path,
      schema = schema,
      barcode_col = "cell_id",
      locus_col = "locus",
      umi_col = "umi_count",
      preprocess = make_default_preprocessing("airr"),
      rename_columns = NULL,
      output_folder = tempfile("airr-")
    )

    print(idata)
    ```

To attach sample information, list your files in a manifest. Here, `study_sample` also defines the repertoire. For your own data, add columns such as patient, tissue, or treatment and choose the appropriate `repertoire_schema`.

=== "R"

    ```r
    manifest <- data.frame(file = path, study_sample = "example")

    idata <- read_repertoires(
      path = "<manifest>",
      manifest = manifest,
      manifest_file_col = "file",
      schema = schema,
      barcode_col = "cell_id",
      locus_col = "locus",
      umi_col = "umi_count",
      preprocess = make_default_preprocessing("airr"),
      rename_columns = NULL,
      repertoire_schema = "study_sample",
      output_folder = tempfile("airr-manifest-")
    )

    print(idata)
    ```
