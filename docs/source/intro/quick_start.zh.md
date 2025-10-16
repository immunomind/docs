# 快速上手（Quick Start）

五分钟导览：加载 `immunarch`，获取示例数据，运行核心分析，并使用随包提供的 `immundata` 工具摄取 AIRR 数据。

## 1) 加载工具包

=== "R"

    ```r
    library(immunarch)
    ```

## 2) 获取示例数据并设置分组

=== "R"

    ```r
    # 小型演示数据集
    idata <- get_test_idata() |> agg_repertoires("Therapy")

    # 打印精简摘要
    idata
    ```

## 3) 初步分析（First-look analyses）

=== "R"

    ```r
    # 基因使用（例如 V 基因）
    airr_stats_genes(idata, gene_col = "v_call") |> vis()

    # 公共性 / 重叠
    airr_public_jaccard(idata) |> vis()

    # 克隆性（丰度分箱）
    airr_clonality_prop(idata)

    # 多样性（均匀度）
    airr_diversity_pielou(idata) |> vis()
    ```

## 4)（可选）按受体注释克隆性并在 Seurat 中绘图

=== "R"

    ```r
    # 添加每受体的克隆性标签
    idata <- annotate_clonality_prop(idata)

    # 按条形码把标签拷贝到 Seurat 对象并给 UMAP 上色
    #（假设你在流程早前已创建了 `sdata`）
    sdata <- annotate_seurat(idata, sdata, cols = "clonal_prop_bin")
    Seurat::DimPlot(sdata, reduction = "umap", group.by = "clonal_prop_bin", shuffle = TRUE)
    ```

## 5)（可选）使用随包的数据层摄取 AIRR 数据

`immundata` 与 `immunarch` 一起发布。你可以直接调用其读取函数以灵活导入。

=== "R"

    ```r
    # 读取 AIRR TSV（示例）
    md_path <- system.file("extdata/tsv", "metadata.tsv", package = "immundata")
    files <- c(
        system.file("extdata/tsv", "sample_0_1k.tsv", package = "immundata"),
        system.file("extdata/tsv", "sample_1k_2k.tsv", package = "immundata")
    )

    md <- read_metadata(md_path)
    idata <- read_repertoires(
    path     = files,
    schema   = c("cdr3_aa", "v_call"),
    metadata = md
    )

    # 继续进行 immunarch 分析
    idata |> agg_repertoires("Therapy") |> airr_clonality_prop()
    ```

## 后续步骤（Next steps）

* 查看我们的详细[教程](../tutorials/single_cell.md)。