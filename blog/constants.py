import platform

server = "Linux" in platform.platform()


DEFAULT_TITLE = "Island"
MAIN_URL = "https://jiangmiemie.com" if server else "http://localhost:3000"
BACKEND_URL = (
    "https://pyneconebackend.jiangmiemie.com" if server else "http://localhost:8000"
)
SPACE_URL = "https://space.jiangmiemie.com/"
CONTACT_URL = "mailto:jiangyangcreate@gmail.com"
GITHUB_URL = "https://github.com/jiangmiemie"
CSR_URL = "https://jiangmiemie.github.io/Computer-Selfeducation-Road/"
MUSIC_URL = "//music.163.com/outchain/player?type=0&id=8415918242&auto=1&height=70"
