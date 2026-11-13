# Installation

This guide installs the toolkit `immunarch` for Adaptive Immune Receptor Repertoire (AIRR) data analysis along with its dependencies. The package  `immundata` for storing and manipulating AIRR datasets ships with `immunarch` and loads automatically, so you do not need to install it separately.

## Requirements

=== "R"

    * R ≥ 4.2 recommended

## Installation

### 1) Install the package installer

=== "R"

    `pak` is the recommended installer for R packages.

    ```r
    install.packages("pak", repos = sprintf("https://r-lib.github.io/p/pak/stable/%s/%s/%s", .Platform$pkgType, R.Version()$os, R.Version()$arch))
    ```

### 2) Install `immunarch`

Install the latest release or the development version.

=== "R"

    ```r
    # Install from CRAN when available
    pak::pak("immunarch")
    ```

    ```r
    # Alternatively, install the latest GitHub build if you are a power user of PC
    pak::pak("immunomind/immunarch")
    ```

    ```r
    # The bleeding edge version -- careful, could be unstable (but so cooler...)
    pak::pak("immunomind/immunarch@dev")
    ```

## Reproducible environments

Pin an exact version (tag or SHA) in your workflows and installation scripts for papers and CI.

=== "R"

    ```r
    pak::pak("immunomind/immunarch@0.9.1")
    ```

## Old `immunarch` versions

The latest pre-v1 version of `immunarch` which should work with the old code is `0.9.1`. You can install it by providing the exact tag `0.9.1`. Please mind that no guarantees on the stability or lack of bugs for this version are given due to multiple dependency packages updated since the `0.9.1` release.

=== "R"

    ```r
    pak::pak("immunomind/immunarch@0.9.1")
    ```

<!-- >
## Useful ecosystem packages

The ecosystem provides several packages for convenience and expanded functionality in addition to the core `immunarch` and `immundata`.

<!-- immundapter -->

<!-- immunread -->

## Next steps

* Load and analyse your data in [quick start](./quick_start.md).

* Read how to load immune repertoire of [different formats](../howto/io/read_airr_bulk.md).

...
...