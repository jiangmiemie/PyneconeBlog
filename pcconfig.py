import pynecone as pc
from blog import constants

config = pc.Config(
    app_name="blog",
    port=3000,
    backend_port=8000,
    api_url=constants.BACKEND_URL,
    frontend_packages=[
        "react-colorful",
        "react-confetti",
        "react-loading-icons",
    ],
)
