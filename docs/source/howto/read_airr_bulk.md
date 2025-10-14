# Load bulk sequencing immune repertoire data in AIRR-C format to `immunarch` in R

Use this for bulk AIRR Rearrangement TSVs (one row per rearrangement/receptor). Requirements: installed `immunarch`.

**How it works:**

* Reads all AIRR-C TSVs from a folder (bulk mode).
* Maps AIRR fields (e.g., `v_call`, `j_call`, `junction_aa`) to a receptor schema.
* Uses the provided count column to set receptor abundance.

**Key arguments:**

* `schema`: features you need (e.g., `junction_aa`, `v_call`, `j_call`)
* `path`: file, glob, or folder with your files
* `count_col`: usually `umi_count` or `duplicate_count` (adjust if your column name differs)

=== "R"

    ```r
    library(immundata)

    schema <- make_receptor_schema(features = c("junction_aa", "v_call"))
    # Alternative:
    schema <- make_receptor_schema(features = c("cdr3_aa", "v_call"))

    idata <- read_repertoires(
      path       = "/path/to/bulk_airr/*.tsv",
      schema     = schema,
      count_col  = "umi_count",
      preprocess = make_default_preprocessing("airr")
    )

    # If you have metadata, you can use it:
    idata <- read_repertoires(
      path       = "/path/to/bulk_airr/*.tsv",
      metadata   = your_metadata_table,
      schema     = schema,
      count_col  = "umi_count",
      preprocess = make_default_preprocessing("airr")
    )

    # If you already know the repertoire schema:
    idata <- read_repertoires(
      path              = "/path/to/bulk_airr/*.tsv",
      metadata          = your_metadata_table,
      schema            = schema,
      count_col         = "umi_count",
      preprocess        = make_default_preprocessing("airr"),
      repertoire_schema = c("Patient", "Cluster", "Response")
    )
    ```