# Annotate

The key functions for annotations are `annotate` and `annotate_immundata`. Functions `annotate_receptors()`, `annotate_barcodes()` and `annotate_chains()` are light-weight wrappers around `annotate_immundata()`. Annotations assign passed values to specified receptors, e.g., gene expression or pattern matched values.

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

### Annotate by any column

=== "R"

    ```r
    idata2 <- annotate(idata = idata, annotations = cells[c("barcode", "ident")], by = c(imd_barcode = "barcode"), keep_repertoires = FALSE)
    idata2 <- idata2 |> filter(!is.na(ident))
    idata2 <- idata2 |> agg_repertoires(schema = "ident")
    
    print(idata2)
    ```
    
### Annotate by receptor identifiers

=== "R"

    ```r
    idata2 <- annotate_receptors(idata = idata, annotations = tibble::tibble(receptor = c(1,2,3), important_data = c("A", "B", "C")), annot_col = "receptor")
    
    idata2 |> filter(important_data %in% c("A", "B"))
    ```
    
### Annotate by barcodes

=== "R"

    ```r
    idata2 <- annotate_barcodes(idata = idata, annotations = cells[c("barcode", "ident")],  annot_col = "barcode", keep_repertoires = FALSE)
    idata2 <- idata2 |> filter(!is.na(ident))
    idata2 <- idata2 |> agg_repertoires(schema = "ident")
    
    print(idata2)
    ```