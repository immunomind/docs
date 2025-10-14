## Load single-cell AIRR-C with loci (TRA/TRB pairing) to immunarch in R

Use this when your single-cell data export is AIRR-C and includes cell barcodes and a `locus` column.

**How it works:**

* Reads AIRR-C TSV with one row per contig.
* Groups by barcode, pairs by `locus` (e.g., `TRA` + `TRB`). Alternatively, selects the specified locus only.
* Picks the top contig per locus using a UMI/read column.

**Key arguments:**

* `schema`: features you need (e.g., `junction_aa`, `v_call`, `j_call`)
* `path`: file, glob, or folder with your files
* `barcode_col`: column with barcodes - `cell_id`
* `locus_col`: column iwht loci information - `"locus"`
* `umi_col`: column with UMI information, usually it is either `umi_count` or `duplicate_count`

=== "R"

    ```r
    library(immundata)

    # If you have two chains, you can select one and filter out others:
    schema <- make_receptor_schema(features = c("junction_aa", "v_call"), chains = c("TCRA"))
    # Or you can create paired-chain receptors:
    schema <- make_receptor_schema(features = c("junction_aa", "v_call"), chains = c("TCRA", "TCRB"))

    idata <- read_repertoires(
      path        = "/path/to/sc_airr/*.tsv",
      schema      = schema,
      barcode_col = "cell_id",
      locus_col   = "locus",
      umi_col     = "umi_count",
      preprocess  = make_default_preprocessing("airr")
    )

    # If you have metadata, you can use it:
    idata <- read_repertoires(
      path        = "/path/to/sc_airr/*.tsv",
      schema      = schema,
      metadata  = your_metadata_table,
      barcode_col = "cell_id",
      locus_col   = "locus",
      umi_col     = "umi_count",
      preprocess  = make_default_preprocessing("airr")
    )

    # If you already know the repertoire schema:
    idata <- read_repertoires(
      path        = "/path/to/sc_airr/*.tsv",
      schema      = schema,
      metadata  = your_metadata_table,
      barcode_col = "cell_id",
      locus_col   = "locus",
      umi_col     = "umi_count",
      preprocess  = make_default_preprocessing("airr"),
      repertoire_schema = c("Patient", "Cluster", "Response")
    )
    ```