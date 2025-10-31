# Reading single- and paired-chain data

`immundata` can represent receptors in multiple ways, as specified in the "Receptor schema" section. Controlling what and how you read is done by passing correct schema and column names to `read_repertoires`. 

Cheat-sheet for arguments to `read_repertoires`:

| Situation                                         | `barcode_col` | `locus_col` | `umi_col` | `chains`         |
| ------------------------------------------------- | ------------- | ----------- | --------- | ---------------- |
| Bulk data, no locus filtering                     | no            | no          | no        | omit / `NULL`    |
| Pair TRA+TRB data, analyse TRA only               | **yes**¹      | **yes**     | no        | `"TRA"`          |
| Pair TRA+TRB data, pick best chain pair per cell  | **yes**       | **yes**     | **yes**   | `c("TRA","TRB")` |
| Pair IGH+IGL\|IGK, pick best chain pair per cell  | **yes**       | **yes**     | **yes**   | `c("IGH","IGL\|IGK")` |

¹ If you pass barcodes, they're stored but used for counting only.


## Chain-agnostic

Used for bulk or pre-filtered immune repertoire data. No filtering by chain data such as TRA or TRB. Each unique combination of features in the schema vector is assigned a unique receptor identifier and counts as a receptor. In the example below, the receptor features are "cdr3_aa" and "v_call" columns - CDR3 amino acid sequence and V gene segment columns respectively.

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

> Please note that single-chain option does not (!) remove multiple chains per cell - yet.
> In other words, you will get multiple receptors per barcode. The paired chain option filter out
> chains which don't have the max number of reads or umis per barcode. So receptor numbers and sequences
> could differ significantly.

Used for paired-chain data such as single-cell data to focus on the analysis of immune receptors with a specific chain. The data is pre-filtered to leave the data units with the specified chain only.

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

When you want full αβ (or heavy‑light) receptors, immundata can pair two chains that originate from the same barcode and keep, for each locus, the chain with the highest UMI/reads. A single unique receptor identifier is then assigned to the pair. The data is pre-filtered to loci in target chains. Within each barcode×locus the the chain with max umis or reads is selected. Barcodes lacking either chain are dropped from the receptor table.

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