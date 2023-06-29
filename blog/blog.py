import pynecone as pc
from blog import styles
from blog.base_state import State
from blog.middleware import CloseSidebarMiddleware

from blog.openai import openairoutes
from blog.openai.login import LoginState

from blog.pages import routes
from blog.components.scripts import *

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
for route in openairoutes:
    print(
        route.path,
    )
    app.add_page(
        route.component,
        route.path,
        route.title,
        on_load=LoginState.check_login() if not route.path.endswith("login") else None,
    )

# Add the middleware.
app.add_middleware(CloseSidebarMiddleware(), index=0)

# Run the app.
app.compile()
