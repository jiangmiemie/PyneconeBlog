import pynecone as pc
from blog.templates.page import imgpage, docheader, doctext, component_grid


@imgpage()
def code():
    return pc.box(
        docheader("编码", first=True),
        doctext("记录了一些代码学习记录"),
        pc.divider(),
        component_grid("code"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
    )
