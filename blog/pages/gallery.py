import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def gallery():
    return pc.box(
        component_grid("gallery"),
        padding="1em 4em",
    )
