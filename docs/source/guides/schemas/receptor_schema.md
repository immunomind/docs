# Receptor schema

`immundata` lets you decide what a receptor means for your study by specifying:

 - Feature columns - which fields make a receptor unique. Usually it is `cdr3_aa` and `v_call` columns.

 - Chains to keep / pair - e.g. `TRA` only or a pair `TRA + TRB`.

You define the receptor schema at the beginning of the analysis when you read the immune repertoire files. All downstream tasks will use the defined receptor schema. If you want to change the receptor definition, e.g., move from a strict `cdr3_aa + v_call` to more relaxed `cdr3_aa` schema, you need to re-read your data from the disk to create a separate `ImmunData` object.


## Chain-agnostic

Used for bulk or pre-filtered immune repertoire data. No filtering by chain data such as `TRA` or `TRB`. Each unique combination of features in the schema vector is assigned a unique receptor identifier and counts as a receptor. In the example below, the receptor features are `cdr3_aa` and `v_call` columns - CDR3 amino acid sequence and V gene segment columns respectively.

=== "R"

    ```r
    library(immundata)
        
    inp_file <- system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata")

    schema <- c("cdr3_aa", "v_call")
        
    idata <- read_repertoires(
        path   = inp_file,
        schema = schema
    )
        
    print(idata)
    ```

## Single-chain

Used for paired-chain data such as single-cell data to focus on the analysis of immune receptors with a specific locus. The data is pre-filtered to leave the data units with the specified locus only.

=== "R"

    ```r
    library(immundata)
        
    inp_file <- system.file("extdata/single_cell", "lt6.csv.gz", package = "immundata")

    schema <- make_receptor_schema(
        features = c("cdr3", "v_call"),
        chains   = "TRA"
    )

    idata <- read_repertoires(
        path        = inp_file,
        schema      = schema,
        barcode_col = "barcode",
        locus_col   = "locus"
    )

    print(idata)
    ```

## Paired-chain

When you want full αβ (or heavy‑light) receptors, `immundata` can pair two chains that originate from the same barcode.

=== "R"

    ```r
    library(immundata)

    inp_file <- system.file("extdata/single_cell", "lt6.csv.gz", package = "immundata")

    schema <- make_receptor_schema(
        features = c("cdr3", "v_call"),
        chains   = c("TRA", "TRB")
    )

    idata <- read_repertoires(
        path        = inp_file,
        schema      = schema,
        barcode_col = "barcode",
        locus_col   = "locus",
        umi_col     = "umis"
    )

    print(idata)
    ```

## Paired-chain – multiple second loci

Ig repertoire analysis requires a specific processing paired-chain data: `IGH` chains can be paired with either `IGK` or `IGL` chains. To handle this scenario, you can provide both chains using special syntax.

=== "R"

    ```r
    library(immundata)

    inp_file <- system.file("extdata/single_cell", "lt6.csv.gz", package = "immundata")

    schema <- make_receptor_schema(
        features = c("cdr3", "v_call"),
        chains   = c("IGH", "IGK|IGL")
    )

    idata <- read_repertoires(
        path        = inp_file,
        schema      = schema,
        barcode_col = "barcode",
        locus_col   = "locus",
        umi_col     = "umis"
    )

    print(idata)
    ```