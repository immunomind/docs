# 在 R 的 `immunarch` 中加载 AIRR-C 格式的批量测序免疫受体库数据

适用于批量 AIRR Rearrangement TSV（每行一个重排/受体）。前提：已安装 `immunarch`。

**工作原理：**

* 从文件夹读取所有 AIRR-C TSV（批量模式）。
* 将 AIRR 字段（如 `v_call`、`j_call`、`junction_aa`）映射到受体 schema。
* 使用提供的计数字段设置受体丰度。

**关键参数：**

* `schema`：你需要的特征（例如 `junction_aa`、`v_call`、`j_call`）
* `path`：文件、通配符（glob）或包含文件的文件夹
* `count_col`：通常是 `umi_count` 或 `duplicate_count`（若列名不同请相应调整）

=== "R"

    ```r
    library(immunarch)

    schema <- make_receptor_schema(features = c("junction_aa", "v_call"))
    # 备选：
    schema <- make_receptor_schema(features = c("cdr3_aa", "v_call"))

    idata <- read_repertoires(
      path       = "/path/to/bulk_airr/*.tsv",
      schema     = schema,
      count_col  = "umi_count",
      preprocess = make_default_preprocessing("airr")
    )

    # 如果你有元数据，可以这样使用：
    idata <- read_repertoires(
      path       = "/path/to/bulk_airr/*.tsv",
      metadata   = your_metadata_table,
      schema     = schema,
      count_col  = "umi_count",
      preprocess = make_default_preprocessing("airr")
    )

    # 如果你已经知道受体库（repertoire）schema：
    idata <- read_repertoires(
      path              = "/path/to/bulk_airr/*.tsv",
      metadata          = your_metadata_table,
      schema            = schema,
      count_col         = "umi_count",
      preprocess        = make_default_preprocessing("airr"),
      repertoire_schema = c("Patient", "Cluster", "Response")
    )
    ```
