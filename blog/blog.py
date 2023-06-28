import pynecone as pc
from blog import styles
from blog.base_state import State
from blog.pages import routes
from blog.middleware import CloseSidebarMiddleware
from blog.components.scripts import *
from blog.constants import MAIN_URL
from blog.datas.datas import *
from blog.openai.openai import chatgpt, dalle


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

app.add_page(
    chatgpt(),
    "chat",
    "Openai",
    description="永远怀着一颗学徒的心",
    meta=[
        {
            "http_equiv": "Content-Security-Policy",
            "content": "upgrade-insecure-requests",
        },
    ],
    image="logo.png",
)
app.add_page(
    dalle(),
    "dalle",
    "Openai",
    description="永远怀着一颗学徒的心",
    meta=[
        {
            "http_equiv": "Content-Security-Policy",
            "content": "upgrade-insecure-requests",
        },
    ],
    image="logo.png",
)

# Add the middleware.
app.add_middleware(CloseSidebarMiddleware(), index=0)

# Run the app.
app.compile()
