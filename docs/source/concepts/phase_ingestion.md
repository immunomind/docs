# Phase 1: Ingestion

```
      ┌───────┐
      │ files │
      └───────┘
          │
          ▼
   read_metadata()    ──── Read metadata
          │
          ▼ 
  read_repertoires()  ──┬─ Read repertoire files (!)
          │             │      ▼
          │             │  Preprocess
          │             │      ▼
          │             │  Aggregate receptors (!)
          │             │      ▼
          │             │  Postprocess
          │             │      ▼
          │             │  Aggregate repertoires #1
          │             │      ▼
          │             └─ Write data on disk (!)
          ▼
   agg_repertoires()  ──── Aggregate repertoires #2
          │
          ▼
    ┌───────────┐
    │ ImmunData │
    └───────────┘
```

Steps marked with `(!)` are non-optional.

The goal of the **ingestion phase** is to turn a folder of AIRR-seq files into an immutable on-disk `ImmunData` dataset.

  1) **Read metadata:**
  
      `read_metadata()` pulls in any sample- or donor-level information, such as therapy arm, HLA type, age, etc., and stores it in a data frame that we can pass to the main reading functions `read_repertoires`. Attaching this context early means every chain you read later already "knows" which patient or time-point it belongs to.
  
      You can safely skip it if you don't have per-sample pr per-donor metadata.
  
  2) **Read repertoire files:**
  
      `read_repertoires()` streams Parquet/CSV/TSV files straight into DuckDB that powers `ImmunData` objects.
  
  3) **Preprocess:**
  
      During the read step you may pass a `preproc = recipe` argument to `read_repertoires` to preprocess data before aggregating receptors: drop unused columns, strip non-productive sequences, translate field names to the AIRR schema, de-duplicate contigs, etc. Because this logic is declarative, re-runs produce identical results.
  
  4) **Aggregate receptors:**
  
      Receptor schema is how you define a receptor – a logical unit of analysis. The `read_repertoires` collapses chains into receptors accordingly and assigns each a stable unique identifier.
      
  3) **Postprocess:**
  
      A mirror step to **preprocess**: a convenient hook to run QC checks, add derived fields, attach reference-gene annotations, or compute per-chain quality metrics **after** the dataset is ready. You can pass any number of steps which will be executed in a sequential order.
  
  5) **Aggregate repertoires #1:**
  
      If you already know how to group chains into receptors, perhaps by `"Sample"` or `"Donor"` columns from the metadata, you can pass `repertoire_schema = c("Sample")` to `read_repertoires()`. Otherwise, skip and define repertoires later (common in single-cell workflows where you need cluster labels first).
      
  3) **Write data on disk:**
  
      `read_repertoires` always persists what it just built: column-compressed Parquet parts plus a human-readable metadata in JSON. From here on, downstream steps can reopen the dataset instantly without touching the raw AIRR files again.
    
  5) **Aggregate repertoires #2:**
  
      Call `agg_repertoires()` later if you withheld grouping until additional annotations were available, e.g. donor + cell cluster.