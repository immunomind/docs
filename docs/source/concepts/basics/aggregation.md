# Aggregation: defining receptors and repertoires

When your data come out of an AIRR assembly tool like **Cell Ranger**, you get many separate V(D)J **chains**.
But most questions are about **receptors** (e.g., “this αβ TCR”) or **repertoires** (e.g., “all receptors from donor A on day 30”).

As with "receptors as logical units", the underlying assumption the second concept is based upon is *researchers work with rearrangements/chains but think in receptors*. `immundata` helps you move from raw chains to these higher-level objects using **controlled aggregation**. This means you set clear rules for how to combine chains, and the software applies those rules without hiding where the data came from.

## `agg_receptors()`: define what “one receptor” means

Use `agg_receptors()` to decide how to build a receptor in your study, what *one receptor* means in your study.

1. You start by choosing a **schema** (a recipe). Examples:
  * Single chain without a V gene segment.
  * Single chain **with** a V gene segment.
  * Pair chains that share the same **barcode** and have α and β loci.
  * Match each **IGH** with the **IGL** that has the same CDR3 amino-acid sequence.
2. The function rebuilds or **re-aggregates** the data and returns a new `ImmunData` object.
  Your old definition stays untouched, the underlying data is not changed.
3. Each receptor gets a stable ID and keeps links to its original chains and barcode.
4. If you change your definition later, just rerun this step. You do not need to edit the rest of your pipeline.

## `agg_repertoires()`: group receptors into meaningful sets

Use `agg_repertoires()` to say how receptors should be grouped for analysis to **repertoires**.

* Example groups: all receptors from one biopsy, from responders to therapy, from a single-cell cluster, or any mix of metadata columns.
* The result is a physical table `idata$repertoires` with basic counts (chains, barcodes, unique receptors).
  Each repertoire keeps direct links to the receptors it contains. So, again, no underlying data is changed — only light-weight annotations on top of it.

## Why this design helps

* **Easy and precise:** You can compute metrics (Jaccard similarity, diversity, etc.) and the exact receptor definition (for example, `"cdr3+v"`) is saved with the result. This reduces human-made mistakes, as you don't need to input the same receptor schema `"cdr3+v"` each time you compute something.

* **Full data lineage by design:**

  * Every receptor knows which chains it includes.
  * Every repertoire knows which receptors it includes.
  * The full “recipe” is stored in the object metadata.
    Six months later – or six reviewers later – you can trace any summary statistic back to the precise chains that produced it, enabling fully reproducible pipelines with no hidden transformations.