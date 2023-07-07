import pynecone as pc
from web import constants
from web.base_state import State, CloseSidebarMiddleware
from web.openai import openairoutes
from web.pgsql import pgsqlroutes
from web.openai.login import LoginState
from web import routes
from web.scripts import *

# Create the app.
app = pc.App(
    state=State,
    style=constants.BASE_STYLE,
    stylesheets=constants.STYLESHEETS,
)

# simple app.
for route in pgsqlroutes + routes:
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

# login app.
for route in openairoutes:
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
