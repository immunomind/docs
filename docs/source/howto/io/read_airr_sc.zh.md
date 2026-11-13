# 在 R 的 `immunarch` 中加载 AIRR-C 格式的单细胞测序免疫受体库数据

当你的单细胞数据导出为 AIRR-C，且包含细胞条形码与 `locus` 列时使用此方法。

**工作原理：**

* 读取 AIRR-C TSV（每行一个 contig）。
* 按条形码分组，并按 `locus` 配对（例如 `TRA` + `TRB`）。或仅选择指定的位点。
* 使用 UMI/reads 列为每个位点选取排名最高的 contig（top contig）。

**关键参数：**

* `schema`：你需要的特征（例如 `junction_aa`、`v_call`、`j_call`）
* `path`：文件、通配符（glob）或包含文件的文件夹
* `barcode_col`：包含条形码的列——`cell_id`
* `locus_col`：包含位点信息的列——`"locus"`
* `umi_col`：包含 UMI 信息的列，通常是 `umi_count` 或 `duplicate_count`

=== "R"

    ```r
    library(immunarch)

    # 如果你有两条链，可以只选择其中一条并过滤其他：
    schema <- make_receptor_schema(features = c("junction_aa", "v_call"), chains = c("TCRA"))
    # 或创建配对链受体：
    schema <- make_receptor_schema(features = c("junction_aa", "v_call"), chains = c("TCRA", "TCRB"))

    idata <- read_repertoires(
      path        = "/path/to/sc_airr/*.tsv",
      schema      = schema,
      barcode_col = "cell_id",
      locus_col   = "locus",
      umi_col     = "umi_count",
      preprocess  = make_default_preprocessing("airr")
    )

    # 如果你有元数据，可以这样使用：
    idata <- read_repertoires(
      path        = "/path/to/sc_airr/*.tsv",
      schema      = schema,
      metadata    = your_metadata_table,
      barcode_col = "cell_id",
      locus_col   = "locus",
      umi_col     = "umi_count",
      preprocess  = make_default_preprocessing("airr")
    )

    # 如果你已经知道受体库（repertoire）schema：
    idata <- read_repertoires(
      path              = "/path/to/sc_airr/*.tsv",
      schema            = schema,
      metadata          = your_metadata_table,
      barcode_col       = "cell_id",
      locus_col         = "locus",
      umi_col           = "umi_count",
      preprocess        = make_default_preprocessing("airr"),
      repertoire_schema = c("Patient", "Cluster", "Response")
    )
    ```
