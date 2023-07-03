import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def page():
    return pc.box(
        pc.heading("代码"),
        component_grid("code"),
        pc.heading("相册"),
        component_grid("gallery"),
        pc.heading("月记"),
        component_grid("month"),
        padding="1em 4em",
        height="100vh",
    )
