import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def month():
    return pc.box(
        pc.heading("月记", first=True),
        pc.text("记录了一些生活的片段 每月月底更新"),
        pc.divider(),
        component_grid("month"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
        padding_left="10em",
    )
