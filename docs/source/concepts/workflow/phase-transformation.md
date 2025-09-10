# Phase 2: Transformation

```
      ┌───────────┐       ┌────────────────────────────┐
      │ ImmunData │       │ AnnData / Seurat / TCRdist │
      └───────────┘       │ seur@meta.data / adata.obs │
            │             └────────────────────────────┘
            │                             │
            ├─────────────────────────────┘
            │
            ▼
   annotate_immundata()    ──── Import external annotations to ImmunData
            │
            ▼ 
     agg_repertoires()     ──── Aggregate repertoires
            │
            ▼ 
    filter_immundata()     ──── Filter receptors or repertoires
            │
            ▼ 
    mutate_immundata()     ──── Create or modify columns, compute statistics
            │
            │     ┌────────────────┐
            ├────►│ save / plot #1 │
            │     └────────────────┘
            ▼ 
   annotate_immundata()    ──── Annotate ImmunData with the computed statistics
            │
            │     ┌────────────────┐
            ├────►│ save / plot #2 │
            │     └────────────────┘
            │
            ▼
┌────────────────────────┐
│seur@meta.data[:] <- ...│ ──── Export ImmunData annotations
│    adata.obs = ...     │
└────────────────────────┘
```

Transformation is a loop of annotation → modification and computation → visualisation, always producing a new `ImmunData` while leaving the parent intact. That immutability is what turns every notebook into a reproducible pipeline.

  1. **Import external annotations to ImmunData:**
  
      `annotate_immundata()` (or its thin wrappers `annotate_barcodes()` / `annotate_receptors()`) merges labels from Seurat/AnnData/TCRdist/anything that can be expressed as a keyed data frame to the main table, so each chain has a corresponding annotation.
  
  2. **Aggregate repertoires:**
  
      Now that extra labels are present, you might regroup receptors, for example, by donor × cell-state.
  
  3. **Filter receptors or repertoires:**
  
      `filter_immundata()` accepts tidy-verse predicates on chains, receptors, or repertoires.
  
  4. **Create or modify columns, compute statistics:**
  
      On this step, you compute statistics per-repertoire or per-receptor, using input receptor features. There are several scenarios depending on what you try to achieve.
  
      1) use `immunarch` for the most common analysis functions. The package will automatically annotate both **receptors/barcodes/chains** (!) and **repertoires** (!!) if it is possible;
  
      2) simply mutate on the whole dataset using `dplyr` syntax, like compute edit distance to a specific pattern using `mutate_immundata`;
  
      3) more complex compute that requires a function to apply to values and is probably not supported by `duckplyr`. See the [🧠 Advanced Topics](#-advanced-topics) for more details.
      
  4. **Save / plot #1:**
  
      Cache the `ImmunData`. Use `ggplot2` to visualise the statistics, computed from `ImmunData`.
  
  5)  **Annotate ImmunData with the computed statistics:**
  
      `annotate_immundata()` (again) joins the freshly minted statistics back to the canonical dataset.
  
  4. **Save / plot #2:**
  
      Save the `ImmunData` with new annotations to disk. Plot the results of analysis.
  
  6)  **Export ImmunData annotations:**
  
      Write the annotated data back to the cell-level dataset (Seurat / AnnData) for the subsequent analysis. Additionally, you could write the `ImmunData` itself to disk if needed.