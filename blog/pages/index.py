import asyncio
import pynecone as pc
from blog import styles
from blog.base_state import State
from blog.templates.page import webpage


class Confetti(pc.Component):
    """Confetti component."""

    library = "react-confetti"
    tag = "ReactConfetti"
    is_default = True


confetti = Confetti.create


class IndexState(State):
    show_confetti: bool = False

    def start_confetti(self):
        """Start the confetti."""
        self.show_confetti = True
        return self.stop_confetti

    async def stop_confetti(self):
        """Stop the confetti."""
        await asyncio.sleep(5)
        self.show_confetti = False


@webpage(path="/")
def index() -> pc.Component:
    from blog.components.navbar import NavbarState

    return pc.box(
        pc.cond(
            IndexState.show_confetti,
            confetti(),
        ),
        pc.hstack(
            pc.desktop_only(
                pc.container(
                    pc.vstack(
                        pc.text(
                            "更新计划", font_size=styles.H3_FONT_SIZE, font_weight="bold"
                        ),
                        pc.hstack(
                            pc.checkbox("黑夜", is_checked=True),
                            pc.checkbox("音乐", is_checked=True),
                            pc.checkbox("点击", is_checked=True),
                            pc.checkbox("地图", is_checked=True),
                            pc.checkbox("查找", is_checked=True),
                        ),
                        pc.hstack(
                            pc.checkbox("首页", is_checked=True),
                            pc.checkbox("文章", is_checked=True),
                            pc.checkbox("相册", is_checked=True),
                            pc.checkbox("智能", is_checked=True),
                            pc.checkbox(
                                "目录",
                                on_change=IndexState.start_confetti,
                                is_checked=IndexState.show_confetti,
                            ),
                        ),
                    ),
                    padding_x="2em",
                    border_radius="25px ",
                    border="5px  #555",
                    box_shadow="lg",
                    center_content=True,
                    padding_bottom="1em",
                    background_image="code.svg",
                    background_repeat="no-repeat",
                    background_position="right bottom",
                    background_size="6em",
                ),
            ),
            pc.center(
                pc.vstack(
                    pc.image(
                        src=styles.LOGO_URL,
                        width="100px",
                        height="auto",
                        border_radius="25px ",
                        border="5px  #555",
                        box_shadow="lg",
                    ),
                    pc.container(
                        "域名是我昵称的谐音：蒋咩咩",
                        font_size=styles.H4_FONT_SIZE,
                        font_family=styles.TEXT_FONT_FAMILY,
                        text_align="center",
                    ),
                    pc.container(
                        pc.form(
                            pc.input(
                                placeholder="查找文章",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {styles.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                    ),
                    justify="space-evenly",
                ),
                spacing="2em",
            ),
            justify="space-evenly",
        ),
        padding_y="12em",
        width="100%",
        background_image="/grid.png",
        background_repeat="no-repeat",
        background_position="top",
    )
