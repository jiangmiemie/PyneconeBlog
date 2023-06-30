import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def code():
    return pc.box(
        pc.heading("编码", first=True),
        pc.text("记录了一些代码学习记录"),
        pc.divider(),
        component_grid("code"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
        padding_left="10em",
    )
