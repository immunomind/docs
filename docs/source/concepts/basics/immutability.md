# Pipeline-based execution: immutability and materialisation

The explicit data lineage we talked about in concepts 1 & 2 pays its dividend only if every step is re-playable. Or, as we call it, reproducible. To make results reproducible, every analysis step must be easy to **run again**.
In `immundata`-powered pipelines, an analysis is a **pipeline of immutable transformations**:

* Each function returns a **new** `ImmunData` object.
* The original object is not changed.
* The chain of objects records how data moved from raw chains to final numbers.

## On-disk by default, in-memory only when needed

Because immunomics datasets started to regularly outgrow RAM, there are several smart data engineering techniques `immundata` employs:

* Tables are saved on disk as **Parquet** files (a column-compressed format).
* Data are **materialised** (loaded into RAM) only when a calculation needs them. For example, to compute a subset or to output final metrics like overlap indices.
* For medium data (e.g., \~10 GB), this feels “invisible”: **DuckDB** streams from the file and gives you a normal in-memory frame.
* For large data (e.g., \~100 GB), the **same code** still works: heavy joins spill to disk, and intermediate results are **cached** so later steps can reuse them.

## What “pipeline thinking” means day to day

Thinking in immutable pipelines means two things:

* **Create snapshots:** when you hit an expensive step, create and save an intermediate `ImmunData` object using `write_immundata` function. The function will create a new cached `ImmunData` object, and you can use this new object, gaining huge speed-ups. Example: computing **edit distances** to patterns or sequences. If you create a snapshot after that, the distances are saved on disk. If you don't, `immundata` will need to re-compute distances each time you call a transformation or computation on `ImmunData` you are working with, and you know how long distance computations are.
* **Assume re-execution:** Anyone, including your colleague or even future-you on a bigger machine, should be able to run `pipeline.R` end-to-end and get the **exact same result**.

## For developers: hide the plumbing and let users focus on biology

Packages that use `immundata` should expose simple, high-level functions like `compute_diversity()` or `plot_overlap()`.
Users should not need to think about `ImmunData`, DuckDB, or Parquet. Ideally, they never notice there is an on-disk database at all.

Leave the data engineering to the data engineers (and bioinformaticians). Keep your attention on the biology — it’s complex enough already.