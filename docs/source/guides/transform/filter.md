# Filter

The key functions for filtering are `filter()` (`dplyr`-compatible) and `filter_immundata()`, which are the same function with a slightly different arguments due to the necessity to comply with `dplyr` interface. Repertoires are reaggregated automatically. Functions `filter_receptors()` and `filter_barcodes()` are used for conveniently filter receptor and barcode identifiers, correspondingly.

To filter data, you simply pass predicates like in `dplyr`. Optionally, you can pass `seq_options` that allow you to filter by exact sequence match, regex pattern, or sequence distances using hamming or edit/levenshtein distances. You can pass multiple patterns via `patterns = c("pattern_1", "pattern_2")`.

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

### Filter by any annotation

=== "R"

    ```r
    idata |> filter(v_call == "TRBV2")
    
    idata |> filter(Tissue == "Blood")
    ```
    
### Chain filters together

=== "R"

    ```r
    # this expression:
    idata |> filter(v_call == "TRBV2", imd_proportion >= 0.0002)
    
    # is the same as this one:
    idata |> filter(v_call == "TRBV2") |> filter(imd_proportion >= 0.0002)
    ```
    
### Filter by sequence distance

=== "R"

    ```r
    idata |> filter(seq_options = make_seq_options(patterns = "CASSELAGYRGEQYF", query_col = "cdr3", method = "lev", max_dist = 3))
    
    idata |> filter(v_call == "TRBV2", seq_options = make_seq_options(patterns = "CASSELAGYRGEQYF", query_col = "cdr3", method = "lev", max_dist = 3))
    ```
    
### Filter by receptor identifiers

=== "R"

    ```r
    idata |> filter_receptors(c(1,2,3))
    ```
    
### Filter by barcodes

=== "R"

    ```r
    target_bc <- cells$barcode[1:3]
    idata |> filter_barcodes(target_bc)
    ```
    
### Filter by repertoire

=== "R"

    ```r
    idata |> filter(imd_repertoire_id == 1)
    
    idata |> filter(Tissue %in% c("Blood", "Tumor"))