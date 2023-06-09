import pynecone as pc
from blog.templates.page import imgpage, docheader, doctext, component_grid


@imgpage()
def month():
    return pc.box(
        docheader("月记", first=True),
        doctext("记录了一些生活的片段 每月月底更新"),
        pc.divider(),
        component_grid("month"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
    )
