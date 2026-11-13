# Load bulk sequencing immune repertoire data in AIRR-C format to `immunarch` in R

The [AIRR Rearrangement format](https://docs.airr-community.org/en/stable/datarep/rearrangements.html) stores immune receptor sequences and annotations in TSV files. `read_airr_bulk()` imports bulk AIRR data with rearrangement sequences and their abundance.

The specification documents the [TSV input structure](https://docs.airr-community.org/en/stable/datarep/rearrangements.html#file-format-specification) and the meaning of each annotation field.

**Installation:**

```r
install.packages("pak")
pak::pak("immunomind/immunread")
```

**How it works:**

- The function returns an `ImmunData` object with one row per retained chain after filtering out non-productive sequences.
- The function uses `duplicate_count` for abundance when present, otherwise `umi_count`. If neither is supplied, each input row represents one observed chain.

AIRR names such as `v_call`, `d_call`, `j_call`, `junction`, and `junction_aa` are unchanged. The count column also keeps its original name. Use these names in your receptor schema.

## Quick start with immunread

**Key arguments:**

- `path`: the input file or a glob matching several files.
- `schema`: receptor features using AIRR column names.
- `column_profile`: defaults to `"standard"`. Set it to `"full"` to keep all source columns.
- `output_folder`: where to store the imported data. The example uses a temporary directory.

=== "R"

    ```r
    library(immunread)

    path <- system.file(
      "extdata", "airr", "2.0-bulk", "contigs.tsv.gz",
      package = "immunread", mustWork = TRUE
    )
    schema <- c("v_call", "junction_aa")

    idata <- read_airr_bulk(
      path = path,
      schema = schema,
      output_folder = tempfile("immunread-")
    )

    print(idata)
    ```

Replace `path` with your own file or a glob such as `"/path/to/bulk_airr/*.tsv"`. Choose a permanent `output_folder` when you want to keep the imported data.

## Advanced: read_repertoires()

Use `immundata::read_repertoires()` directly when you want to choose the input columns and preprocessing yourself. This is also the reader used by `immunread`.

**Key arguments:**

- `path`: your input file or glob, or `"<manifest>"` to read files listed in a manifest.
- `schema`: the receptor features and loci to analyse.
- `count_col`: the abundance column, such as `"duplicate_count"` or `"umi_count"`. Choose the column that represents abundance in your data.
- `preprocess`: transformations applied before receptor construction.
- `manifest`: an optional table of file paths and sample information.
- `repertoire_schema`: columns that define your repertoires, such as patient or tissue.

This example uses the same bundled file and sets the column names explicitly.

=== "R"

    ```r
    library(immundata)

    path <- system.file(
      "extdata", "airr", "2.0-bulk", "contigs.tsv.gz",
      package = "immunread", mustWork = TRUE
    )
    schema <- c("v_call", "junction_aa")

    idata <- read_repertoires(
      path = path,
      schema = schema,
      count_col = "duplicate_count",
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
      count_col = "duplicate_count",
      preprocess = make_default_preprocessing("airr"),
      rename_columns = NULL,
      repertoire_schema = "study_sample",
      output_folder = tempfile("airr-manifest-")
    )

    print(idata)
    ```
