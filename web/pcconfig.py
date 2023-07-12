import reflex as pc
from web import constants

config = pc.Config(
    app_name="web",
    port=3000,
    backend_port=8000,
    api_url=constants.BACKEND_URL,
    frontend_packages=[
        "react-confetti",
    ],
)
