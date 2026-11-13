# Convert `immunarch::repLoad()` output to `ImmunData` in R

[immunarch](https://immunarch.com/) is an R toolkit for immune repertoire analysis. `from_immunarch()` converts repertoire lists produced by the older `repLoad()` interface into an `ImmunData` object.

**How it works:**

* The function takes an `immunarch::repLoad()` object (`imm`) as input.
* It writes one TSV file per repertoire to `temp_folder` and adds a filename column.
* It imports these TSV files into an `ImmunData` object using `read_repertoires()`.
* It saves the data as Parquet files in `output_folder` and returns the `ImmunData` object.

**Key arguments:**

* `imm`: output of `immunarch::repLoad()`.
* `output_folder`: where Parquet data will be stored (auto-created).
* `schema`: character vector defining **unique receptor keys**
  The default is `c("CDR3.aa", "V.name")`, and you can add `"J.name"` if needed.
* `temp_folder`: where intermediate TSVs are written (defaults to a temp dir).

=== "R"

    ```r
    library(immunarch)

    # 1) Load your immunarch object (reads all repertoires + optional metadata)
    immdata <- immunarch::repLoad("/path/to/your/files")

    # 2) Convert to ImmunData (Parquet-backed), customizing receptor key if needed
    idata <- from_immunarch(
      imm           = immdata,
      schema        = c("CDR3.aa", "V.name"),
      output_folder = "/path/to/immundata_out"
    )

    idata
    ```

Optionally, you can rename the columns in your `immdata` object before passing to `from_immunarch` to align it with AIRR-C format:

=== "R"

    ```r
    rename_to_airr <- function(df) {
      map <- c(
        "CDR3.aa"   = "cdr3_aa",
        "CDR3.nt"   = "cdr3_nt",
        "V.name"    = "v_call",
        "D.name"    = "d_call",
        "J.name"    = "j_call",
        "Clones"    = "umi_count",
        "Read.count"= "duplicate_count",
        "Barcode"   = "cell_id",
        "barcode"   = "cell_id",
        "Chain"     = "locus",
        "Gene"      = "locus",
        "Productive"= "productive"
      )

      present_old <- intersect(names(df), names(map))
      if (!length(present_old)) return(df)

      new_names <- unname(map[present_old])
      keep <- !duplicated(new_names)
      present_old <- present_old[keep]
      new_names    <- new_names[keep]

      spec <- stats::setNames(rlang::syms(present_old), new_names)
      dplyr::rename(df, !!!spec)
    }

    immdata$data <- lapply(immdata$data, rename_to_airr)
    ```
