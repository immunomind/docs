```r
    #| label: load-dataset-types-10x
    #| eval: false
    
    #
    # AIRR-C
    #
    schema <- make_receptor_schema(features = c("junction_aa", "v_call"), chains = "TCRB")
    # or
    schema <- make_receptor_schema(features = c("cdr3_aa", "v_call"), chains = "TCRB")
    # reminder how to read paired-chain data if needed:
    schema <- make_receptor_schema(features = c("cdr3_aa", "v_call"), chains = c("TCRA", "TCRB"))
    
    idata <- read_repertoires(path = inp_files, 
                              schema = schema, 
                              metadata = md_table,
                              barcode_col = "cell_id",
                              locus_col = "locus",
                              umi_col = "umi_count", 
                              preprocess = make_default_preprocessing("airr"), 
                              repertoire_schema = "Tissue")
    
    #
    # 10XGenomics
    #
    
    # This is how the original schema would look like
    schema <- make_receptor_schema(features = c("cdr3_aa", "v_gene"), chains = "TRB")
    
    idata <- read_repertoires(path = inp_files, 
                              schema = schema, 
                              metadata = md_table, 
                              barcode_col = "barcode", 
                              locus_col = "chain", 
                              umi_col = "umis", 
                              preprocess = make_default_preprocessing("10x"),
                              rename_columns = NULL,
                              repertoire_schema = "Tissue")
    
    # Immundata renames some columns by default to match them with AIRR-C format.
    # So we use this:
    schema <- make_receptor_schema(features = c("cdr3", "v_call"), chains = "TRB")
    
    idata <- read_repertoires(path = inp_files, 
                              schema = schema, 
                              metadata = md_table, 
                              barcode_col = "barcode", 
                              locus_col = "locus", 
                              umi_col = "umis", 
                              preprocess = make_default_preprocessing("10x"),
                              repertoire_schema = "Tissue")
    ```



---

# Load 10x Genomics V(D)J (single locus) to `immunarch` in R

**Intro:** Use this to keep only one locus (e.g., TRB) from 10x `filtered_contig_annotations.csv`.

**What happens**

* Reads 10x contig annotations.
* Selects one locus per barcode (e.g., TRB).
* Optionally chooses the best contig by UMI/read count.

**Key arguments**

* `path`: `filtered_contig_annotations.csv`
* `barcode_col`: `"barcode"`
* `locus_col`: `"chain"`
* `umi_col` (optional): e.g., `umis` or `reads`
* `schema`: restrict to the locus you want (e.g., `"TRB"`)

```r
library(immunarch)

schema <- make_receptor_schema(features = c("v_call", "j_call", "cdr3"), chains = "TRB")
idata <- read_repertoires(
  path        = "/path/to/filtered_contig_annotations.csv",
  schema      = schema,
  barcode_col = "barcode",
  locus_col   = "chain",
  umi_col     = "umis"              # or "reads", if present
)
```

---

# Load 10x Genomics V(D)J (paired TRA+TRB) to `immunarch` in R

**Intro:** Use this to build paired α/β repertoires from 10x contig annotations.

**What happens**

* Reads 10x contigs per barcode.
* Selects the top TRA and the top TRB per barcode (by UMI/reads if provided).
* Produces paired receptors per cell.

**Key arguments**

* `path`: `filtered_contig_annotations.csv` (or `all_contig_annotations.csv`)
* `barcode_col`: `"barcode"`
* `locus_col`: `"chain"`
* `umi_col` (recommended): e.g., `umis` or `reads`
* `schema`: expect both loci (`TRA`, `TRB`)

```r
library(immunarch)

schema <- make_receptor_schema(features = c("cdr3"), chains = c("TRA", "TRB"))
idata <- read_repertoires(
  path        = "/path/to/filtered_contig_annotations.csv",
  schema      = schema,
  barcode_col = "barcode",
  locus_col   = "chain",
  umi_col     = "umis"              # recommended for best-contig selection
)
```

---

If you want, I can add tiny “verify” snippets (e.g., check locus distribution, pairing rate) right under each recipe.
