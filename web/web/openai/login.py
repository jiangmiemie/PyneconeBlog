import pynecone as pc
from web.base_state import State as BS
from web.page import webpage
from web.constants import MAIN_URL


class LoginState(BS):
    username: str
    password: str
    flag = False

    def login(self):
        """Log in a user."""
        if self.username == "admin" and self.password == "admin":
            self.flag = True
            return pc.redirect(f"{MAIN_URL}/openai/chatgpt")
        else:
            return pc.window_alert("Invalid username or password.")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.flag:
            return pc.redirect(f"{MAIN_URL}/openai/login")


@webpage()
def login():
    return pc.box(
        pc.container(
            pc.heading(
                pc.span("Welcome to Openai"),
                display="flex",
                flex_direction="column",
                align_items="center",
                text_align="center",
            ),
            pc.box(
                pc.input(
                    placeholder="Username : admin",
                    on_blur=LoginState.set_username,
                    mb=4,
                ),
                pc.input(
                    type_="password",
                    placeholder="Password : admin",
                    on_blur=LoginState.set_password,
                    mb=4,
                ),
                pc.button(
                    "Log in",
                    on_click=LoginState.login,
                    bg="blue.500",
                    color="white",
                    _hover={"bg": "blue.600"},
                ),
                align_items="left",
                border="1px solid #eaeaea",
                p=4,
                max_width="400px",
                border_radius="lg",
            ),
            border_top_radius="lg",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            py=12,
            gap=4,
        ),
        h="100vh",
        pt=16,
        background="url(bg.svg)",
        background_repeat="no-repeat",
        background_size="cover",
    )
