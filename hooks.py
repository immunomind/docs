import re

try:
    import mkquartodocs.plugin as mq
except Exception:
    mq = None

if mq and hasattr(mq, "MkQuartodocsConfig"):

    def _cfg_contains(self, key):
        return isinstance(key, str) and hasattr(self, key)

    def _cfg_getitem(self, key):
        if not isinstance(key, str):
            raise KeyError(key)
        return getattr(self, key)

    mq.MkQuartodocsConfig.__contains__ = _cfg_contains
    mq.MkQuartodocsConfig.__getitem__ = _cfg_getitem

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
