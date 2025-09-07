import re

# Quarto wrapper lines:
#  ::: {.cell}               (open)
#  ::: {.cell-output ...}    (open)
#  :::                        (close)   or  ::::
RE_OPEN = re.compile(
    r"^[ \t]*:::+[ \t]*\{[ \t]*\.(?:cell|cell-output)\b[^}]*\}[ \t]*$", re.M
)
RE_CLOSE = re.compile(r"^[ \t]*:::+[ \t]*$", re.M)

# Normalize Pandoc-style fences like:
#   ``` {.python .cell-code}  ->  ```python
#   ``` {.r .cell-code}       ->  ```r
RE_FENCE_ATTR = re.compile(
    r"^```[ \t]*\{[ \t]*\.([A-Za-z0-9_+-]+)[^}]*\}[ \t]*$", re.M
)


def on_page_markdown(markdown, page, config, files):
    # 1) strip Quarto's cell wrappers (only those with .cell/.cell-output)
    md = RE_OPEN.sub("", markdown)
    md = RE_CLOSE.sub("", md)

    # 2) turn Pandoc attribute fences into plain language fences
    md = RE_FENCE_ATTR.sub(lambda m: f"```{m.group(1)}", md)

    return md
