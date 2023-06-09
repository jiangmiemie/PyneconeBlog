import pynecone as pc
from blog.templates.page import imgpage, docheader, doctext, component_grid


@imgpage()
def gallery():
    return pc.box(
        docheader("相册", first=True),
        doctext("记录了一些美好的画面"),
        pc.divider(),
        component_grid("gallery"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
    )
