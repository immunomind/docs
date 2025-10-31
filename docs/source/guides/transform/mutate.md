# Mutate

The key functions for this are `mutate` (`dplyr`-compatible) / `mutate_immundata` and the functions from the downstream analysis tools. Mutations change one or several columns, or add new columns. This is what is called `with_columns` in `polars`.

Run this code before running examples below:

=== "R"

    ```r
    library(immundata)
        
    inp_files <- paste0(system.file("extdata/single_cell", "", package = "immundata"), "/*.csv.gz")
    md_file <- system.file("extdata/single_cell", "metadata.tsv", package = "immundata")
    md_table <- read_metadata(md_file)
    cells_file <- system.file("extdata/single_cell", "cells.tsv.gz", package = "immundata")
    cells <- readr::read_tsv(cells_file)

    schema <- make_receptor_schema(features = c("cdr3", "v_call"), chains = c("TRB"))

    idata <- read_repertoires(
        path              = inp_files, 
        schema            = schema, 
        metadata.         = md_table, 
        barcode_col       = "barcode", 
        locus_col         = "locus", 
        umi_col           = "umis", 
        preprocess        = make_default_preprocessing("10x"), 
        repertoire_schema = "Tissue")
    ```

### Add or transform one or several annotation columns

=== "R"

    ```r
    idata |> mutate(new_column = "value")
    
    idata |> mutate(big_chains = umis >= 10)
    
    # You can use duckdb functions via `dd$<function>`
    idata |> mutate(dist_to_pattern = dd$levenshtein(cdr3, "CASSSVSGNSPLHF"))
    ```
    
### Add columns with sequence distance to patterns

=== "R"

    ```r
    patterns <- c("CASSVHPQYF", "CAWSGQGWGGSTDTQYF", "CASSPRPGSTGELFF")
    idata |> mutate(seq_options = make_seq_options(query_col = "cdr3", patterns = patterns, method = "lev"))
    
    idata |> mutate(seq_options = make_seq_options(query_col = "cdr3", patterns = patterns, method = "lev", name_type = "pattern"))
    ```
    
### Modify a subset of column values

=== "R"

    ```r
    idata |> mutate(found_pattern = if_else(cdr3 == "CASSVHPQYF", 1, 0))
    ```