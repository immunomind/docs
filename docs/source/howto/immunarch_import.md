# Convert immunarch `repLoad` output to ImmunData in R

Use this to migrate your **immunarch v0.9** repertoires into an **ImmunData** dataset from `immunarch 0.10/1.0`.

**How it works:**

* Takes an `immunarch::repLoad()` object (`imm`).
* Writes one **TSV per repertoire** (adds a filename column) to `temp_folder`.
* Imports those TSVs with `read_repertoires()` into **ImmunData**.
* Saves Parquet files under `output_folder`; returns an **ImmunData** object.

**Key arguments:**

* `imm`: output of `immunarch::repLoad()`.
* `output_folder`: where Parquet data will be stored (auto-created).
* `schema`: character vector defining **unique receptor keys**
  (default `c("CDR3.aa", "V.name")`; you can add `"J.name"`).
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

Optionally, you can rename the columns in your `immdata` object before passing to `from_immunarch` to align it with AIRR-C format.
