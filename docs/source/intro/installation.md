# Installation

This guide installs the **analysis toolkit** `immunarch` for repertoire analysis. The **data layer** `immundata` ships with `immunarch` and loads automatically, so you do not need to install it separately for typical workflows. Advanced users will find optional `immundata` install steps at the end.

## Requirements

* R ≥ 4.2 recommended
* Internet access to install packages

## 1) Install `pak` (recommended installer)

=== "R"

    ```r
    install.packages("pak", repos = sprintf("https://r-lib.github.io/p/pak/stable/%s/%s/%s", .Platform$pkgType, R.Version()$os, R.Version()$arch))
    ```

## 2) Install `immunarch` (includes `immundata`)

Use the GitHub build if you want the newest features.

=== "R"

    ```r
    # Latest GitHub build
    pak::pkg_install("immunomind/immunarch")

    # Or install from CRAN when available
    pak::pkg_install("immunarch")
    ```

### Verify the installation

=== "R"

    ```r
    library(immunarch)
    packageVersion("immunarch")
    # immundata is bundled; it will be available when you load immunarch
    ```

### Reproducible environments

Pin an exact version (tag or SHA) for papers and CI:

=== "R"

    ```r
    pak::pkg_install("immunomind/immunarch@v0.9.1")
    ```

## Optional: install `immundata` alone

Only needed if you want to work directly with the data layer API, build ingestion pipelines, or contribute.

=== "R"

    ```r
    # Latest GitHub build
    pak::pkg_install("immunomind/immundata")

    # Or CRAN when available
    pak::pkg_install("immundata")

    # Pin a specific version
    pak::pkg_install("immunomind/immundata@0.2.1")
    ```