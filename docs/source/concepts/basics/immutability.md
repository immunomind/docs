# Pipeline-based execution: immutability and materialisation

We talked a lot about data traceability or data lineage in the first two concepts. But it makes sense to implement the data lineage only if every workflow step is re-playable. Or, as we call it, reproducible. To make results reproducible, every analysis step must be easy to run again without any side effects, when the underlying data is changed.
In `immundata`-powered pipelines, an analysis is a **pipeline of immutable transformations**:

* Each function returns a **new** `ImmunData` object.
* The underlying data is not changed. New object – new view into the data.
* The chain of `ImmunData` objects records how data moved from raw chains to final numbers.

## On-disk by default, in-memory only when needed

Immutability is not very convenient at the first glance, but it allows us to work with larger-than-RAM immune repertoire datasets. There are several smart data engineering techniques `immundata` employs:

* Immune data tables are saved on disk as **Parquet** files (a column-compressed format, meaning faster data analysis).
* Dataset is materialised (i.e., loaded into RAM) only when a calculation needs them. For example, to compute a subset or to output final metrics like overlap indices.
* For medium data (e.g., ~10 GB), this feels "invisible": **DuckDB** (the lightweight database `immundata` uses as a backend) streams from the file and gives you a normal in-memory frame.
* And for large data (e.g., ~100 GB), the same code still works because the whole magic with Parquet and views into the data allows DuckDB to efficiently query the underlying data without loading unnecessary parts to RAM.

A trade-off is clear: you either work in RAM like you did with typical data frames, with RAM being your limiting factor; or you create immutable transformations, allowing DuckDB to optimize processing queries, leading to the out-of-memory data support.

## What "pipeline thinking" means day to day

Thinking in immutable pipelines means two things:

* **Create snapshots:** when you hit an expensive step, create and save an intermediate `ImmunData` object using `immundata::write_immundata()` function. The function will create a new `ImmunData` object, and you can use this new object, gaining huge speed-ups. Example: computing edit distances to patterns or sequences. If you create a snapshot after that, the distances are saved on disk. If you don't, `immundata` will need to re-compute distances each time you call a transformation or computation on `ImmunData` you are working with, and you know how long distance computations are.

* **Assume re-execution:** Anyone, including your colleague or even future-you on a bigger machine, should be able to run `pipeline.R` end-to-end and get the exact same result.

## For developers: hide the plumbing and let users focus on biology

Packages that use `immundata` should expose simple, high-level functions like `compute_diversity()` or `plot_overlap()`.
Users should not need to think about `ImmunData`, DuckDB, or Parquet. Ideally, they never notice there is an on-disk database at all.

Leave the data engineering to the data engineers (and bioinformaticians). Keep your attention on the biology — it’s complex enough already.