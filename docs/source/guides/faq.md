# F.A.Q.

## Performance – speed, memory

1. **Q: My workflows are slow! But you promised the new `immunarch` and `immundata` would be faster!**

    A: There are a few cases where `immunarch 1.0` (powered by `immundata`) may be slower than `immunarch 0.9` or other tools.

    - If your dataset is small, the overhead of managing DuckDB can be larger than the computation itself.

    - Remember *immutability*? If you don't create snapshots to cache results, the **entire pipeline (including file reads)** will run again. That may be why it feels slower. Create snapshots with `immundata::write_immundata()` after heavy steps. For example, when you're done annotating with scRNA-seq clusters or other metadata, save the updated `ImmunData` to disk so those steps don't rerun.

    You can run `duckplyr::explain(idata$annotations)` to see the query plan. If it's long and hard to scroll, that's a good sign you should snapshot.

    It can feel inconvenient at first, but it gets easier. If anything is unclear, open an issue, and I'll add tutorials and best-practice guides. The benefits of this `dplyr`-like, immutable workflow are worth it.


## Data – reading, writing, formats, engineering

1.  **Q: Why do we need `ImmunData` when there are `AnnData` and `MuData`?**

    A: `ImmunData` doesn’t try to replace AnnData or MuData. It solves a **different problem**.
    AnnData/MuData are great for **cell × gene** data. `ImmunData` is built for **AIRR** data-things like **receptors, clonotypes, chains, and repertoires**.

    * **Receptor-first and AIRR-aligned.**
    `ImmunData` follows the AIRR Community schema (with a small superset). Field names are stable and clear, so you can share data and methods across tools without guessing what a column means.

    * **Aggregation is a core feature.**
    You can **define a repertoire on the fly** (by sample, tissue, timepoint, therapy, etc.) and re-aggregate quickly. Counts and proportions then become **well defined per repertoire**, which is essential for clonality, diversity, and publicity.

    * **Works for bulk and single-cell.**
    It handles bulk repertoires and scAIRR, supports **multiple chains per barcode**, pairing rules, and explicit clonotype definitions. When you need to show results in Seurat or AnnData, you simply **join by `barcode`** and, for example, **colour a UMAP** with receptor labels.

    * **Modern data engineering by default.**
    Data live in **Parquet/Arrow**, queries run through **DuckDB**, and we use **lazy evaluation**. This means the pipeline **scales beyond RAM** and only **materialises** when needed. With **snapshots (immutability)** you can freeze expensive steps for speed and reproducibility.

    * **Ready for ML/DL.**
    It’s straightforward to build **feature tables** (V/J usage, k-mers, CDR3 embeddings, etc.) and export them as **Parquet** for training in Python, Julia, or R—no messy conversions.

    * **Interoperable, not overlapping.**
    Keep gene-expression matrices in **Seurat/AnnData**. Keep AIRR receptors in **`ImmunData`**. **Join by barcode** when you want the two worlds together. Each tool does what it’s best at.

    * **Focused scope.**
    Heavy or niche analyses can live in small extension packages. The core stays lean, stable, and easier to install.

    > **When not to use it:**
    > For **very small datasets** (where Arrow/DuckDB overhead may dominate) or for workflows that never touch **AIRR concepts** (pure transcriptomics).

    **In short:** AnnData/MuData manage **cells and genes**. `ImmunData` manages **receptors and repertoires**. They work best **together**.

2.  **Q: How does `immundata` works under the hood, in simpler terms?**

    A: Picture a three-layer sandwich:
    
    - `Parquet` files in `Arrow` column-compressed format hold the raw tables on the disk.

    - `DuckDB` is an in-process SQL engine that can query those files without loading them fully into RAM.

    - `duckplyr` glues `dplyr` verbs (filter, mutate, summarise, …) to DuckDB SQL, so your R code looks exactly like a tidyverse pipeline while the heavy lifting happens in C++.

    When you call `read_repertoires()`, `immundata` reads `Parquet` files, registers them with `DuckDB`, and returns a `duckplyr` table – a data frame-like structure that is in reality a lightweight database connection to `DuckdDB`. Every later operation is lazily translated into SQL - a special language for quering databases. Nothing is materialised (i.e., computed and output) until a workflow step truly needs physical data (e.g. a plot or an algorithm that exists only in R).

    References:

    1. [Arrow for R – columnar file format](https://arrow.apache.org/docs/r/)

    2. [DuckDB – embedded analytical database](https://duckdb.org/)

    3. [duckplyr – API/implementation details](https://duckplyr.tidyverse.org/index.html)

3.  **Q: Why do you need to create Parquet files with receptors and annotations?**

    A: Those are intermediate files, optimized for future data operations, and working with them significantly accelerates `immundata`.

4.  **Q: Why does `immundata` support only the AIRR-C file format?!**

    A: The short answer is because a single, stable schema beats a zoo of drifting ones.
    
    The practical answer is that `immundata` allows some optionality – you can provide column names for barcodes, etc.
    
    The long answer is that the amount of investments required not only for the development, but also for the continued support of parsers for different formats, is astonishing. I developed parsers for 10+ formats for `tcR` / `immunarch` packages. I would much prefer for upstream tool developers not to change their format each minor version, breaking pretty much all downstream pipelines and causing all sorts of pain to end users and tools developers – mind you, without bearing a responsibility to at least notify, but ideally fix the broken formats they introduced. The time of the Wild West is over. The AIRR community did an outstanding job creating its standard. Please urge the creators of your favourite tools or fellow developers to use this format or a superset, like `immundata` does.

    `immundata` does not and will not explicitly support other formats. This is both a practical stance and communication of crucial values, put into `immundata` as part of a broader ecosystem of AIRR tools. The domain is already too complex, and we need to work together to make this complexity manageable. A healthy ecosystem is not the same as a complex ecosystem.

4.  **Q: What do I do then? I really need the output from package `X` in `immunarch`...**

    A: In the previous question, I outlined the motivation behind focusing on AIRR-C format only.

    There are four practical steps that you can do:

    * (recommended) Ask the maintainer of the package `X` to support the AIRR-C file format. It is not that hard to implement.
    
    * Use `read_repertoires` from `immundata` and create your own reader. Helpful links: [`read_repertoires` reference](https://immunomind.github.io/immundata/reference/read_repertoires.html) and the [full documentation website](https://immunomind.github.io/docs/).

    * Use the community-driven package `work-in-progress` to read files as it provides more parsers. Link: TBD

    * If `work-in-progress` doesn't support the desired file format, you can create your own parser using `read_repertoires` and contribute it to `work-in-progress`. I personally would greatly appreciate it.

12. **Q: Why are the counts for receptors available only after all the aggregation?**

    A: Counts and proportions are properties of a receptor inside a specific repertoire. A receptor seen in two samples will be counted twice – once per repertoire. Until receptors and repertoires are defined, any "count" would be ambiguous. That's why the numbers appear only after `agg_receptors()` and `agg_repertoires()` have locked those definitions in.

7.  **Q: You filter out non-productive receptors. How do I explore them?**

    A: Disable filtering of non-productive receptors in the `preprocess` step of `read_repertoires()`.

8.  **Q: Why does `immundata` have its own column names for receptors and repertoires? Could you just use the AIRR format - repertoire_id etc.?**

    A: The power of `immundata` is fast re-aggregation, which lets you define what repertoire means on the fly via `agg_repertoires()`. That's why we use a superset of AIRR field names, which is totally acceptable as per their documentation.

9.  **Q: What do I do with following error: "Error in `compute_parquet()` at [...]: ! ?***

    A: It means that your repertoire files have different schemas, i.e., different column names. You have two options.

    **Option 1:** Check the data and fix the schema. Explore the reason why the data have different schemas. Remove wrong files. Change column names. And try again.

    **Option 2:** If you know what you are doing, pass argument `enforce_schema = FALSE` to `read_repertoires`. The resultant table will have NAs in the place of missing values. But don't use it without considering the first option. Broken schema usually means that there are some issues in how the data were processed upstream.


## Interface – functions, methods, naming

1.  **Q: Why all the function names or ImmunData fields are so long? I want to write `idata$rec` instead of `idata$receptors`.**

    A: Two main reasons: readability and encouraging autocomplete. Use your IDE's **Tab** to trigger autocomplete; it can speed you up 10–20×.

5.  **Q: Why is it so complex? Why do we need to use `dplyr` instead of plain R?**

   A: The short answer is:
   - faster computations;
   - code that is easy to maintain and support by other humans;
   - better data skills by thinking in immutable transformations;
   - in most cases you don't need complex transformations, so we can optimise ~95% of AIRR operations behind the scenes.

6.  **Q: How do I use `dplyr` operations that `duckplyr` doesn't support yet?**

    A: Let's consider several use cases.

    **Case 0.** You are missing `group_by` from `dplyr`. Use `summarise(.by = ???, ...)`.

    **Case 1.** Your data can fit into RAM. Call `collect` and use `dplyr`.

    **Case 2.** Your data won't fit into RAM but you must run a heavy operation on all rows. You can rewrite functions in SQL. You can break it into supported pieces (e.g. pre-filter, pre-aggregate) that DuckDB can stream, write an intermediate Parquet with `compute_parquet()`, then loop over chunks, collect them, and run the analysis.

    **Case 3.** Your data won't fit into RAM, but before running intensive computations, you are open to working with smaller dataset first. Filter down via `slice_head(n=...)`, iterate until the code works, then run the same pipeline on the full dataset.


## Miscellaneous

10. **Q: `immundata` is too verbose, I'm tired of all the messages. How to turn them off?**
    
    A: Run the following code `options(rlib_message_verbosity = "quiet")` in the beginning of your R session to turn off messages.

11. **Q: I don't want to use `pak`, how can I use the good old `install.packages` or `devtools`?**

    A: Nothing will stop you, eh? You are welcome, but I'm not responsible if something won't work due to issues with dependencies:

    ```r
   # CRAN release
   install.packages("immundata")
   library(immundata)

   # GitHub release
   install.packages("devtools")
   devtools::install_github("immunomind/immundata")
   library(immundata)

   # Development version (dev branch)
   devtools::install_github("immunomind/immundata", ref = "dev")
   library(immundata)
   ```