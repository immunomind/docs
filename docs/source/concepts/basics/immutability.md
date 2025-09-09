# Pipeline-based execution: immutability and materialisation

The explicit data lineage we talked about in concepts 1 & 2 pays its dividend only if every step is re-playable. That is why `immundata` treats an analysis as a *pipeline of immutable transformations*. Each function returns a fresh `ImmunData` object, leaving the parent untouched; the full chain of objects records how the data travelled from raw chains to final statistics.

Because immunomics datasets started to regularly outgrow RAM, those objects do **not** live in memory by default. Their tables are persisted as column-compressed Parquet files and "materialised" – pulled into RAM – only when a computation truly needs them, typically to crunch a subset or to emit the final numbers such as repertoire-overlap indices. For a 10 GB dataset that fits in memory, this behaviour is invisible: DuckDB streams the file, you get an in-memory frame, and life goes on. For a 100 GB experiment, the same code still runs; the heavy joins spill to disk, and the intermediate results are cached so downstream steps can reuse them without recomputation.

Thinking in pipelines therefore means two things:

- **Cache what matters:** create intermediate `ImmunData` objects when you hit an expensive step, and write them to disk; the next run can pick up from there. A prime example of this a computing edit distances to some patterns or sequences.

- **Assume re-execution:** any colleague (or future-you on a bigger cluster) should be able to rerun `pipeline.R` end-to-end without interactive tinkering and arrive at the same result byte-for-byte.

All of this engineering should stay behind the curtain. Downstream packages that adopt `immundata` as their backbone should expose high-level verbs such as `compute_diversity()` or `plot_overlap()`; the user need not touch `ImmunData`, DuckDB, or Parquet. In the ideal scenario they never learn that an on-disk database powers their workflow – and they never have to.

Leave the data engineering to the data engineers (and, sadly, bioinformaticians – I feel your pain); keep your focus or the focus of your users on the biology. It is sophisticated enough already.