import pynecone as pc
from blog import styles
from blog.base_state import State
from blog.pages import routes
from blog.middleware import CloseSidebarMiddleware
from blog.components.scripts import *
from blog.constants import MAIN_URL
from blog.datas.datas import travellast
from blog.openai import openai


# Create the app.
app = pc.App(
    state=State,
    style=styles.BASE_STYLE,
    stylesheets=styles.STYLESHEETS,
)

for route in routes:
    app.add_page(
        route.component,
        route.path,
        route.title,
        description="永远怀着一颗学徒的心",
        meta=[
            {
                "http_equiv": "Content-Security-Policy",
                "content": "upgrade-insecure-requests",
            },
        ],
        image="logo.png",
        script_tags=[
            scripts(),
        ],
    )

app.add_page(travellast, route="travellast", title="travellast")
app.add_page(openai.openai(), route="openai", title="Openai", image="openai.png")

app.add_custom_404_page(
    pc.center(
        pc.link(
            pc.vstack(
                pc.text("没有找到你要的内容", font_size=styles.H1_FONT_SIZE, font_weight="bold"),
                pc.text("不妨回主页看看", font_size=styles.H3_FONT_SIZE, font_weight="bold"),
            ),
            href=MAIN_URL,
        ),
        padding_y="3em",
    ),
    title=404,
    description="Sorry , it not a open url",
)

# Add the middleware.
app.add_middleware(CloseSidebarMiddleware(), index=0)

# Run the app.
app.compile()
