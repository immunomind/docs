# Quick Start

A five‑minute tour of `immunarch`: ingest the AIRR data, compute statistics, annotate the data, and create visualisations.

## 1) Load the package

Happy analyses are all alike. They all begin with...

=== "R"

    ```r
    library(immunarch)
    ```

## 2) Get example data and define a repertoire

A first look into the new design philosophy of `immunarch` — you are the one who decides what a repertoire is. The simplest solution it so just provide all columns from your `manifest.csv` file, previously known as `metadata.txt`.

=== "R"

    ```r
    # Small demo dataset
    idata <- get_test_idata() |> agg_repertoires("Therapy")

    # Print a compact summary
    idata
    ```

## 3) Analyse and visualise

And be happy (hopefully).

=== "R"

    ```r
    # Gene usage (e.g., V gene)
    airr_desc_genes(idata, gene_col = "v_call") |> vis()

    # Publicity / overlap
    repsim_bray(idata) |> vis()

    # Clonality (proportion bins)
    airr_clonality_prop(idata)

    # Diversity (evenness)
    airr_diversity_pielou(idata) |> vis()
    ```

## 4) Annotate clonality per receptor and plot in Seurat

If you have an scRNAseq data, you can annotate `SeuratObject` or `AnnData`.

=== "R"

    ```r
    # Add per‑receptor clonality labels
    idata <- annotate_clonality_prop(idata)

    # Copy labels to a Seurat object by barcode and color UMAP
    # (Here we assume you created `sdata` earlier in your workflow)
    sdata <- annotate_seurat(idata, sdata, cols = "clonal_prop_bin")
    Seurat::DimPlot(sdata, reduction = "umap", group.by = "clonal_prop_bin", shuffle = TRUE)

    # adata <- annotate_anndata(idata, adata, cols = "clonal_prop_bin")
    ```

## 5) Ingest AIRR data with the bundled data layer

For the learning purposes, please see the example on how to load immune repertoires into `immunarch` using the new function `read_repertoires()`. Please mind that not only you decide what a repertoire is, you also have a power to decide a receptor is – single-chain, paired-chain, with or without additional Ig light chain, use Variable gene segment or not, and so on.

=== "R"

    ```r
    # Read the bundled manifest and AIRR TSVs
    manifest_path <- system.file(
        "extdata/tsv", "manifest.csv", package = "immundata"
    )
    manifest <- read_manifest(manifest_path)

    idata <- read_repertoires(
        path          = "<manifest>",
        schema        = c("cdr3_aa", "v_call"),
        manifest      = manifest,
        count_col     = "counts",
        output_folder = tempfile("immundata-quick-start-")
    )

    # Continue with immunarch analyses
    idata |> agg_repertoires("Therapy") |> airr_clonality_prop()
    ```

## Next steps

* Explore the detailed [tutorials](../tutorials/single_cell.md).

* Read the [in-depth guide](../guides/schemas/receptor_schema.md) on the data analysis philosophy and design decisions.
