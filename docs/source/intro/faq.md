# F.A.Q.

1.  **Q: My workflows are slow! But you promised that new `immunarch` and `immundata` should be faster than before!**

    A: There are several scenarios when new `immunarch 1.0` powered by `immundata` could be slower than other tools and `immunarch 0.9`.

    - The data is small, and the overhead for management of DuckDB is bigger than the data analysis computational requirements.

    - Remember "immutability"? If you don't cache your data, the **whole pipeline from input file reading** is run again and again. Considering you haven't noticed it on the previous steps, maybe it tells us something about the true speed of `immundata`. I advise you to create "snapshots" of the data using `immundata::write_immundata` after several computational-heavy steps. For example, when you done annotating your data with scRNAseq cluster or any other information, it would be great to save the new `ImmunData` on the disk so the system won't need to run annotations again next time you call your `ImmunData` object.

    You can run `immdata$annotations |> explain()` to see the query plan. If you get tired scrolling it up, maybe it's a good time to create a snapshot of your data...
    
    I know it's not very easy to grasp and sometimes it's even inconvenient. But I assure you: it gets better. Learn, open an issue so I can make more tutorials explaining best practices, and the benefits of this new, `dplyr`-like methodology will come.


1.  **Q: Why all the function names or ImmunData fields are so long? I want to write `idata$rec` instead of `idata$receptors`.**

    A: Two major reasons – improving the code readability and motivation to leverage the autocomplete tools. Please consider using `tab` for leveraging autocomplete. It accelerates things x10-20.

2.  **Q: How does `immundata` works under the hood, in simpler terms?**

    A: Picture a three-layer sandwich:
    
    - `Arrow` files on disk hold the raw tables in column-compressed Parquet.

    - `DuckDB` is an in-process SQL engine that can query those files without loading them fully into RAM.

    - `duckplyr` glues `dplyr` verbs (filter, mutate, summarise, …) to DuckDB SQL, so your R code looks exactly like a tidyverse pipeline while the heavy lifting happens in C++.

    When you call `read_repertoires()`, immundata writes `Arrow` parts, registers them with `DuckDB`, and returns a `duckplyr` table. Every later verb is lazily translated into SQL; nothing is materialised until a step truly needs physical data (e.g. a plot or an algorithm that exists only in R).

    References
    1. [Arrow for R – columnar file format](https://arrow.apache.org/docs/r/)
    2. [DuckDB – embedded analytical database](https://duckdb.org/)
    3. [duckplyr – API/implementation details](https://duckplyr.tidyverse.org/index.html)

3.  **Q: Why do you need to create Parquet files with receptors and annotations?**

    A: Those are intermediate files, optimized for future data operations, and working with them significantly accelerates `immundata`. I will post a benchmark soon.

4.  **Q: Why does `immundata` support only the AIRR standard?!**

    A: The short answer is because a single, stable schema beats a zoo of drifting ones.
    
    The practical answer is that `immundata` allows some optionality – you can provide column names for barcodes, etc.
    
    The long answer is that the amount of investments required not only for the development, but also for the continued support of parsers for different formats, is astonishing. I developed parsers for 10+ formats for `tcR` / `immunarch` packages. I would much prefer for upstream tool developers not to change their format each minor version, breaking pretty much all downstream pipelines and causing all sorts of pain to end users and tools developers – mind you, without bearing a responsibility to at least notify, but ideally fix the broken formats they introduced. The time of the Wild West is over. The AIRR community did an outstanding job creating its standard. Please urge the creators of your favourite tools or fellow developers to use this format or a superset, like `immundata` does.

    `immundata` does not and will not explicitly support other formats. This is both a practical stance and communication of crucial values, put into `immundata` as part of a broader ecosystem of AIRR tools. The domain is already too complex, and we need to work together to make this complexity manageable. A healthy ecosystem is not the same as a complex ecosystem.

5.  **Q: Why is it so complex? Why do we need to use `dplyr` instead of plain R?**

    A: The short answer is:

    -   faster computations;
    -   code, that is easy to maintain and support by other humans;
    -   better data skills thanks to thinking in immutable transformations,
    -   in most cases you don't really need complex transformations, so we can optimize 95% of all AIRR data operations behind the scenes.

6.  **Q: How do I use `dplyr` operations that `duckplyr` doesn't support yet?**

    A: Let's consider several use cases.

    **Case 0.** You are missing `group_by` from `dplyr`. Use `summarise(.by = ???, ...)`.

    **Case 1.** Your data can fit into RAM. Call `collect` and use `dplyr`.

    **Case 2.** Your data won't fit into RAM but you must run a heavy operation on all rows. You can rewrite functions in SQL. You can break it into supported pieces (e.g. pre-filter, pre-aggregate) that DuckDB can stream, write an intermediate Parquet with `compute_parquet()`, then loop over chunks, collect them, and run the analysis.

    **Case 3.** Your data won't fit into RAM, but before running intensive computations, you are open to working with smaller dataset first. Filter down via `slice_head(n=...)`, iterate until the code works, then run the same pipeline on the full dataset.

7.  **Q: You filter out non-productive receptors. How do I explore them?**

    A: Do not filter out non-productive receptors in `preprocess` in `read_repertoires()`.

8.  **Q: Why does `immundata` have its own column names for receptors and repertoires? Could you just use the AIRR format - repertoire_id etc.?**

    A: The power of `immundata` lies in the fast re-aggregation of the data, that allows to work with whatever you define as a repertoire on the fly via `agg_repertoires`. Hence I use a superset of the AIRR format, which is totally acceptable as per their documentation.

9.  **Q: What do I do with following error: "Error in `compute_parquet()` at [...]: ! ?***

    A: It means that your repertoire files have different schemas, i.e., different column names. You have two options.

    **Option 1:** Check the data and fix the schema. Explore the reason why the data have different schemas. Remove wrong files. Change column names. And try again.

    **Option 2:** If you know what you are doing, pass argument `enforce_schema = FALSE` to `read_repertoires`. The resultant table will have NAs in the place of missing values. But don't use it without considering the first option. Broken schema usually means that there are some issues in the how the data were processed upstream.

10. **Q: `immundata` is too verbose, I'm tired of all the messages. How to turn them off?**
    
    A: Run the following code `options(rlib_message_verbosity = "quiet")` in the beginning of your R session to turn off messages.

11. **Q: I don't want to use `pak`, how can I use the good old `install.packages` or `devtools`?**

    A: Nothing will stop you, eh? You are welcome, but I'm not responsible if something won't work due to issues with dependencies:

    ```r
    # CRAN release
    install.packages("immundata")

    # GitHub release
    install.packages(c("devtools", "pkgload"))
    devtools::install_github("immunomind/immundata")
    devtools::reload(pkgload::inst("immundata"))

    # Development version
    devtools::install_github("immunomind/immundata", ref = "dev")
    devtools::reload(pkgload::inst("immundata"))
    ```

12. **Q: Why are the counts for receptors available only after all the aggregation?**

    A: Counts and proportions are properties of a receptor inside a specific repertoire. A receptor seen in two samples will be counted twice – once per repertoire. Until receptors and repertoires are defined, any "count" would be ambiguous. That's why the numbers appear only after `agg_receptors()` and `agg_repertoires()` have locked those definitions in.