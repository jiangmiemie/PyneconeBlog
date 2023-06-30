import pynecone as pc
from blog.templates.page import webpage, component_grid


@webpage()
def code():
    return pc.box(
        component_grid("code"),
        padding="1em 4em",
    )
