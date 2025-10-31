# Reading repertoire files

`immundata` provides a flexible system for loading immune receptor repertoire files from different sources -- CSV, TSV and Parquet files, possibly gzipped, with some optionality. The main function for this is `read_repertoires()`. Below are four ways to pass your file paths and one for convering data from existing `immunarch pre-1.0` list objects with `$data` and `$meta`.

This section is focused on different ways to work with input files. In the next [section]("modes.smd") we will talk about different data modes – how to read single-chain and paired-chain data in a desired receptor schema.

### Single file

If you just have **one** AIRR file:

=== "R"

    ```r
    library(immundata)
    
    inp_file <- system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata")
    
    idata <- read_repertoires(
        path   = inp_file,
        schema = c("cdr3_aa", "v_call")
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
        path   = file_vec,
        schema = c("cdr3_aa", "v_call")
    )
    
    print(idata)
    ```

`immundata` automatically merges them (depending on your chosen schema), writes the aggregated data into a single directory of Parquet files, and produces a single-cell `ImmunData` object. Think about it as a huge table instead of smaller multiple repertoire tables.

### Glob pattern

If your files follow a consistent naming pattern, you can leverage shell globs:

=== "R"

    ```r
    library(immundata)
    
    folder_with_files <- system.file("extdata/tsv", "", package = "immundata")
    
    glob_files <- paste0(folder_with_files, "sample*.tsv")
    
    print(glob_files)
    # The output is something like "/Library/Frameworks/.../immundata/extdata/tsv/*"
    # Mind the star "*" at the end
    
    # For example, all AIRR files in the 'samples/' folder
    idata <- read_repertoires(
        path   = glob_files,
        schema = c("cdr3_aa", "v_call")
    )
    
    print(idata)
    ```

Behind the scenes, `read_repertoires()` expands the glob with `Sys.glob(...)`, merges the data, and produces a single `ImmunData`.

### Metadata table

Sometimes you need more control over the data source (e.g. consistent sample naming, extra columns). In that case:

1.  **Load metadata** with `read_metadata()`.

2.  **Pass** the resulting data frame to `read_repertoires(path = "<metadata>", ..., metadata = md_table)`. Mind the `"<metadata>"` string we pass to the function. It indicates that we should take file paths from the input metadata table.

An example code:

=== "R"

    ```r
    library(immundata)
    
    md_path <- system.file("extdata/tsv", "metadata.tsv", package = "immundata")
    
    md_table <- read_metadata(md_path)
    
    print(md_table)
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
        path     = "<metadata>",
        metadata = md_table,
        schema   = c("cdr3_aa", "v_call")
    )
    
    print(idata)
    ```

This approach **unifies** sample-level metadata (e.g. donor ID, timepoint) with your repertoire data inside a single `ImmunData`.

You can pass the metadata table separately along with the list of files as we did in the previous examples without the `<metadata>` directive, but in that case you would need to check the correctness of all filepaths by yourself. Which could be quite cumbersome, to say the least.

The more information on how to work with metadata files, please read the next section.

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