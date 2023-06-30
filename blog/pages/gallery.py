import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def gallery():
    return pc.box(
        pc.text("记录了一些美好的画面"),
        pc.divider(),
        component_grid("gallery"),
        text_align="left",
        margin_bottom="4em",
        width="100%",
        padding_left="10em",
    )
