import pynecone as pc
from blog import constants
import platform

server = "Linux" not in platform.platform()

config = pc.Config(
    app_name="blog",
    port=3000,
    backend_port=8000,
    api_url="http://localhost:8000" if server else constants.BACKEND_URL,
    frontend_packages=[
        "react-colorful",
        "react-confetti",
        "react-loading-icons",
    ],
)
