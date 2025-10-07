# Quick Start

A five‑minute tour: load `immunarch`, get example data, run core analyses, and ingest AIRR data with the bundled `immundata` tools.

## 1) Load the toolkit

=== "R"

    ```r
    library(immunarch)
    ```

## 2) Get example data and set a grouping

=== "R"

    ```r
    # Small demo dataset
    idata <- get_test_idata() |> agg_repertoires("Therapy")

    # Print a compact summary
    idata
    ```

## 3) First‑look analyses

=== "R"

    ```r
    # Gene usage (e.g., V gene)
    airr_stats_genes(idata, gene_col = "v_call")

    # Publicity / overlap
    airr_public_jaccard(idata)

    # Clonality (proportion bins)
    airr_clonality_prop(idata)

    # Diversity (evenness)
    airr_diversity_pielou(idata)
    ```

## 4) (Optional) Annotate clonality per receptor and plot in Seurat

=== "R"

    ```r
    # Add per‑receptor clonality labels
    idata <- annotate_clonality_prop(idata)

    # Copy labels to a Seurat object by barcode and color UMAP
    # (Assumes you created `sdata` earlier in your workflow)
    sdata <- annotate_seurat(idata, sdata, cols = "clonal_prop_bin")
    Seurat::DimPlot(sdata, reduction = "umap", group.by = "clonal_prop_bin", shuffle = TRUE)
    ```

## 5) (Optional) Ingest AIRR data with the bundled data layer

`immundata` ships with `immunarch`. You can call its readers directly for flexible ingestion.

=== "R"

    ```r
    # Read AIRR TSVs (toy example)
    md_path <- system.file("extdata/tsv", "metadata.tsv", package = "immundata")
    files <- c(
    system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata"),
    system.file("extdata/tsv", "sample_1k_2k.tsv", package = "immundata")
    )

    md <- immundata::read_metadata(md_path)
    idata <- immundata::read_repertoires(
    path     = files,
    schema   = c("cdr3_aa", "v_call"),
    metadata = md
    )

    # Continue with immunarch analyses
    idata |> agg_repertoires("Therapy") |> airr_clonality_prop()
    ```

## Next steps

* Explore our detailed [Tutorials](../tutorials/single_cell.md).
