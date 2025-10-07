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

**Example:** The old `repDiversity()` function is now a family of functions, each with a clear, shared prefix. For instance, you now call `airr_diversity_shannon()` or `airr_diversity_pielou()`. These functions are still grouped under one help page so you can compare them and discover new metrics easily.

This same idea applies across the package: overlap, clonality, gene usage, and more. You'll find smaller, clearer tools with consistent naming and arguments throughout. The reason is that with huge multi-tool functions it requires a lot of cognitive investment to remember specific method arguments. With smaller function you can effortlessly invoke a help from IDE itself via autocomplete (tab).

* **Watch for deprecations.** If the console says “deprecated” or “will be removed in v1.1.0”, please update your code soon. Compatibility shims are temporary and will eventually be removed.

### 3) Fewer heavy dependencies

Many packages were moved from `Depends` to `Suggests`. As a result, `immunarch` now installs much faster and brings in far fewer dependencies. The 0.9 version would pull in around 140 packages on a clean machine, while 0.10 is closer to 88. If you use a feature that requires an optional package, you'll see a clear prompt telling you what to install.

### 4) Working with visualizations

Functions like `vis()` have been **removed**. This decision wasn't taken lightly: programmatically producing publication-ready plots is extremely challenging, and most users ended up editing the generated plots to fit journal requirements anyway. For examples of what's involved, see [this guide to publication-ready ggplot2](https://github.com/CerrenRichards/ggplot2-for-publications).

Instead, we now provide ggplot2 code templates for common publication figures in the tutorials and guides. This approach not only helps you learn ggplot2 (the standard for scientific plotting in R), but also ensures your figures match your desired style or journal specifications right from the start.

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

* **Outdated code** is hard to maintain—especially in academic environments where developer turnover is high.
* **Improved code culture:** modern best practices, standard data structures, consistent naming.
* **Lazy backends:** DuckDB, Arrow, and other technologies can now be plugged in for performance boosts with large repertoires. Immundata is backend-agnostic by design.
* **Parallelization:** Where possible, immunarch steps will run in parallel out of the box, speeding up your analyses.

---

## Conclusion

`immunarch` 1.0.0 is a major step forward, making immune repertoire analysis **lighter**, **faster**, and **easier to maintain**. Although many changes involve removing heavy dependencies, the core user experience should remain familiar. For larger or more advanced analyses, try out **ImmunData** to take advantage of its robust data structures and efficient transformations.

Stay tuned for updates in **2025**. If you have questions or migration issues, please reach out on GitHub. Thank you!