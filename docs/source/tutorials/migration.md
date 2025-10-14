# Migration from immunarch v0.9 to v1.0

This guide is for existing `immunarch` users. If you're new to `immunarch`, you can safely skip this tutorial.

**Note:** The 0.9.y versions of `immunarch` (e.g., 0.9.1) are no longer supported. If something breaks (e.g., due to a dependency update), it will not be fixed. I highly recommend upgrading to version 0.10 as soon as possible. Version 0.10 serves as a pre-release version for 1.0, and feature parity between 0.9 and 1.0 will be achieved within a few months. Once it is done, the version 0.10.x will be switched to 1.0.

I'm prioritizing feature parity, stability, and enhancements for the most common workflows as well as advanced use cases relevant to immunotherapy development. If you need help with migration or run into issues, please open an issue on GitHub - I'm happy to help.

---

## High-level overview of v1.0 changes

Version 1.0 introduces several important changes compared to the 0.9.x series.

### 1) Working with data

Version 1.0 embraces a much clearer data layer centered on **ImmunData** from `immundata` R package. ImmunData is a lightweight, consistent data structure for working with chains, receptors, and repertoires. It promotes immutability, i.e., functions no longer mutate your data in place, but instead return new objects. This makes pipelines easier to reason about and eliminates hidden side effects, but requires changes in how you **think** about the data analysis. Read more in the **Concepts** section.

ImmunData is designed to be scale-agnostic. Today, you can use small immune repertoire samples; tomorrow, you can plug in larger-than-memory datasets with zero changes to your code. The API remains stable and your analysis code stays simple.

### 2) API changes

Some function signatures have changed. Large, multi-tool functions are now split into smaller, focused ones.

**Example:** The old `repDiversity()` meta-function is now a family of functions, each with a clear, shared prefix. For instance, you now call `airr_diversity_shannon()` or `airr_diversity_pielou()`. These functions are still grouped under one help page so you can compare them and discover new metrics easily. Simply run `?airr_diversity` to get a list of all functions in the family. This holds for virtually all other function families - `?airr_stats`, `?airr_clonality`, `?annotate_clonality`, etc.

You'll find smaller, clearer tools with consistent naming and arguments throughout. The reason is that with huge multi-tool functions such as `repOverlap` it requires a lot of cognitive investment to remember specific method arguments. With smaller function you can effortlessly invoke a help from IDE itself via autocomplete by pressing "tab" while typing the function name.

* **Watch for deprecations.** If the console says "deprecated" or "will be removed in v1.1.0", please update your code soon. Compatibility shims are temporary and will eventually be removed.

### 3) Fewer heavy dependencies

Many packages were moved from `Depends` to `Suggests`. As a result, `immunarch` now installs much faster and brings in far fewer dependencies. The 0.9 version would pull in around 140 packages on a clean machine, while 0.10 is closer to 80. If you use a feature that requires an optional package, you'll see a clear prompt telling you what to install.

### 4) Working with visualizations

The `vis()` function family has not been implemented for the new analysis functions – yet. This was a deliberate choice. The major downside of `vis()` lies in its general nature: sadly, one-size-fits-all didn't work as expected. Programmatically producing publication-ready plots is extremely challenging, and most users end up editing the generated plots to fit journal requirements anyway. For examples of what's involved in preparing plots to publication, see [this guide to publication-ready ggplot2](https://github.com/CerrenRichards/ggplot2-for-publications).

Currently, I provide ggplot2 code templates for common publication figures in the tutorials and guides. This approach not only helps you learn ggplot2 (the standard for scientific plotting in R), but also ensures your figures match your desired style or journal specifications right from the start.

My plan is to update `vis()` to support 1.0 analysis methods. Run `?vis()` to check if something changed and there is no "deprecated" flag. However, the new implementation strategy will be completely different: opinionated and lightweight visualisations in 1.0 instead of heavy and general solutions for all possible use cases in 0.9. In other words, new `vis()` won't be able to produce all kinds of plots. The created plots will serve the major purpose of helping you quickly understand your data, rather than providing all the tweaks and gears for publication-ready plots. And if you want to change something, please use `ggplot2` and read that great guide on publication-ready plots.

* **Where can I find themes and palettes?** Check out [ggsci](https://cran.r-project.org/web/packages/ggsci/vignettes/ggsci.html) and [this curated palette list](https://emilhvitfeldt.github.io/r-color-palettes/) for easy, beautiful color options.

To view the latest migration updates, run `get_immunarch_news()` in your R console.

---

## If you must stay on `immunarch` v0.9

If you absolutely must freeze the last stable version before 1.0, use one of the following installation methods:

* **pak**:

  ```r
  pak::pkg_install("immunarch@=0.9.1")
  ```
* **install.packages**:

  ```r
  install.packages("https://cran.r-project.org/src/contrib/Archive/immunarch/immunarch_0.9.1.tar.gz", repos = NULL, type = "source")
  ```
* **conda**:

  ```bash
  mamba install -c conda-forge r-immunarch=0.9.1
  ```

> Reminder: 0.9.x will receive **no** further updates or fixes.

---

## Why do I even need 1.0?

* **Outdated code** is hard to maintain, especially in academic environments where developer turnover is high. New `immunarch` code is much easier to support and remember what it does.
* **Improved code culture:** modern best practices, standard data structures, consistent naming, and more - all of this in the new ecosystem of tools, where `immunarch` is the core.
* **Lazy backends for large-scale data:** thanks to amazing people behind DuckDB, duckplyr, Arrow and Parquet, `immunarch` now supports out-of-memory datasets without any code changes on your side.
* **Parallelization:** where possible, `immunarch` steps will run in parallel out of the box, speeding up your analyses, efficiently using modern server architecture.

---

Stay tuned for updates in **2025**. If you have questions or migration issues, please reach out on GitHub. Thank you!