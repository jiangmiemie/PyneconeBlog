import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def month():
    return pc.box(
        component_grid("month"),
        padding="1em 4em",
    )
