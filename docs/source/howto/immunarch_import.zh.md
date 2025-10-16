# 在 R 中将 `immunarch::repLoad()` 的输出转换为 `ImmunData`

用于将 **immunarch v0.9** 的受体库迁移为 `immunarch 0.10/1.0` 中的 **ImmunData** 数据集。

**工作原理：**

* 接收一个 `immunarch::repLoad()` 对象（`imm`）。
* 为每个受体库各写出一个 **TSV**（并添加文件名列）到 `temp_folder`。
* 用 `read_repertoires()` 将这些 TSV 导入为 **ImmunData**。
* 在 `output_folder` 下保存 Parquet 文件；返回一个 **ImmunData** 对象。

**关键参数：**

* `imm`：`immunarch::repLoad()` 的输出。
* `output_folder`：存放 Parquet 数据的位置（自动创建）。
* `schema`：定义**唯一受体键**的字符向量
  （默认 `c("CDR3.aa", "V.name")`；你也可以加入 `"J.name"`）。
* `temp_folder`：写入中间 TSV 的位置（默认为临时目录）。

=== "R"

    ```r
    library(immunarch)

    # 1）加载 immunarch 对象（读取所有受体库 + 可选元数据）
    immdata <- immunarch::repLoad("/path/to/your/files")

    # 2）转换为 ImmunData（以 Parquet 为后端），必要时自定义受体键
    idata <- from_immunarch(
      imm           = immdata,
      schema        = c("CDR3.aa", "V.name"),    
      output_folder = "/path/to/immundata_out"
    )

    idata
    ```

可选地，你也可以在把对象传给 `from_immunarch` 之前，先在 `immdata` 中重命名列，使其更贴近 AIRR-C 格式：

=== "R"

    ```r
    rename_to_airr <- function(df) {
      map <- c(
        "CDR3.aa"   = "cdr3_aa",
        "CDR3.nt"   = "cdr3_nt",
        "V.name"    = "v_call",
        "D.name"    = "d_call",
        "J.name"    = "j_call",
        "Clones"    = "umi_count",
        "Read.count"= "duplicate_count",
        "Barcode"   = "cell_id",
        "barcode"   = "cell_id",
        "Chain"     = "locus",
        "Gene"      = "locus",
        "Productive"= "productive"
      )
      
      present_old <- intersect(names(df), names(map))
      if (!length(present_old)) return(df)
      
      new_names <- unname(map[present_old])
      keep <- !duplicated(new_names)
      present_old <- present_old[keep]
      new_names    <- new_names[keep]
      
      spec <- stats::setNames(rlang::syms(present_old), new_names)
      dplyr::rename(df, !!!spec)
    }

    immdata$data <- lapply(immdata$data, rename_to_airr)
    ```
