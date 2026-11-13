# Reading repertoire files

`immundata` provides a flexible system for loading immune receptor repertoire files from different sources -- CSV, TSV and Parquet files, possibly gzipped, with some optionality. The main function for this is `read_repertoires()`. Below are four ways to pass your file paths and one for convering data from existing `immunarch pre-1.0` list objects with `$data` and `$meta`.

This section is focused on different ways to work with input files. In the next [section](modes.md) we will talk about different data modes – how to read single-chain and paired-chain data in a desired receptor schema.

### Single file

If you just have **one** AIRR file:

=== "R"

    ```r
    library(immundata)
    
    inp_file <- system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata")
    
    idata <- read_repertoires(
        path          = inp_file,
        schema        = c("cdr3_aa", "v_call"),
        count_col     = "counts",
        output_folder = tempfile("immundata-")
    )
    
    print(idata)
    ```

### Vector of file names

For **multiple** files in a vector:

=== "R"

    ```r
    library(immundata)
    
    inp_file1 <- system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata")
    inp_file2 <- system.file("extdata/tsv", "sample_1k_2k.tsv", package = "immundata")
    
    file_vec <- c(inp_file1, inp_file2)
    
    idata <- read_repertoires(
        path          = file_vec,
        schema        = c("cdr3_aa", "v_call"),
        count_col     = "counts",
        output_folder = tempfile("immundata-")
    )
    
    print(idata)
    ```

`immundata` combines the files into one `ImmunData` object backed by Parquet storage. The receptor schema determines how receptors are identified, and `count_col` identifies the column containing their abundance.

### Glob pattern

If your files follow a consistent naming pattern, you can leverage shell globs:

=== "R"

    ```r
    library(immundata)
    
    folder_with_files <- system.file("extdata/tsv", "", package = "immundata")
    
    glob_files <- file.path(folder_with_files, "sample*.tsv")
    
    print(glob_files)
    # The output is something like "/Library/Frameworks/.../immundata/extdata/tsv/*"
    # Mind the star "*" at the end
    
    # For example, all AIRR files in the 'samples/' folder
    idata <- read_repertoires(
        path          = glob_files,
        schema        = c("cdr3_aa", "v_call"),
        count_col     = "counts",
        output_folder = tempfile("immundata-")
    )
    
    print(idata)
    ```

Behind the scenes, `read_repertoires()` expands the glob with `Sys.glob(...)`, merges the data, and produces a single `ImmunData`.

### Manifest table

A manifest table contains links to repertoire files with sample-level information such as donor, tissue or treatment. By default, the manifest has a `file` column containing repertoire file paths.

=== "R"

    ```r
    library(immundata)

    manifest_path <- system.file(
        "extdata/tsv", "manifest.csv", package = "immundata"
    )
    manifest <- read_manifest(manifest_path)

    print(manifest)
    ```

    ```
    # The column "File" stores the file paths. If you have a different column name
    # for files, use the `metadata_file_col = "<your column name>"` argument.
    # A tibble: 2 × 5
    File                       Therapy Response Prefix filename
    <chr>                      <chr>   <chr>    <chr>  <chr>   
    1 /.../immundata-/inst/extd… ICI     FR       S1_    /Users/…
    2 /.../immundata-/inst/extd… CAR-T   PR       S2_    /Users/…
    ```

    ```r
    idata <- read_repertoires(
        path          = "<manifest>",
        manifest      = manifest,
        schema        = c("cdr3_aa", "v_call"),
        count_col     = "counts",
        output_folder = tempfile("immundata-manifest-")
    )

    print(idata)
    ```

`path = "<manifest>"` tells `read_repertoires()` to use the paths in the manifest. If the path column has a different name, pass it to both functions: for example, `read_manifest(manifest_path, file_col = "path")` and `read_repertoires(..., manifest_file_col = "path")`.

`read_repertoires()` writes persistent backing files to `output_folder`. If it is omitted, the folder is created beside the first input file. Please mind that reusing an output folder replaces its existing `annotations.parquet` and `metadata.json`. Use a new folder for a separate dataset.

### Convert from `immunarch` format

Pass `immunarch` data lists to `from_immunarch()` to create `ImmunData` objects.

=== "R"

    ```r
    library(immundata)
    # Install old immunarch:
    # pak::pkg_install("immunomind/immunarch@0.9.1")
    data(immdata, package = "immunarch")
    
    idata <- from_immunarch(
        imm = immdata, 
        schema = c("CDR3.aa", "V.name"), 
        output_folder = "./immdata-test"
    )
    
    print(idata)
    ```