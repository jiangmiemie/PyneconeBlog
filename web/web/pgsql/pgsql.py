import asyncio
import pynecone as pc
from web import constants
from web.page import webpage
from web.base_state import State
from web.pgsql.tsclient import client


class NavbarState(State):
    sidebar_open: bool = False

    search_modal: bool = False

    search_input: str = ""

    def change_search(self):
        self.search_modal = not (self.search_modal)

    def toggle_sidebar(self):
        """Toggle the sidebar open state."""
        self.sidebar_open = not self.sidebar_open

    @pc.var
    def search_results(self) -> list[dict[str, dict[str, str]]]:
        if self.search_input == "":
            return []
        return client(self.search_input)


def format_search_results(result):
    return pc.vstack(
        pc.link(
            pc.text(
                result["document"]["heading"],
                font_weight=600,
                color=constants.DOC_HEADER_COLOR,
            ),
            pc.divider(),
            pc.text(
                result["document"]["description"],
                font_weight=400,
                color=constants.DOC_REG_TEXT_COLOR,
            ),
            href=result["document"]["href"],
        ),
        on_click=NavbarState.change_search,
        border_radius="0.5em",
        width="100%",
        align_items="start",
        padding="0.5em",
        _hover={"background_color": "#e3e3e3c"},
    )


def get_search():
    return pc.box(
        pc.form(
            pc.input(
                placeholder="查找文章",
                on_change=NavbarState.set_search_input,
                _focus={
                    "border": f"2px solid {constants.ACCENT_COLOR}",
                },
                backdrop_filter="blur(10px)",
            ),
            on_submit=NavbarState.change_search,
        ),
    )


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


@webpage()
def pgsql() -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.center(
                pc.vstack(
                    pc.button(
                        "重置测试数据",
                        width="50%",
                    ),
                    pc.container(
                        pc.form(
                            pc.input(
                                placeholder="智能查找",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                        pc.form(
                            pc.input(
                                placeholder="数据库语法：查",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                        pc.form(
                            pc.input(
                                placeholder="数据库语法：增删改",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
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
        padding_y="5em",
        width="100%",
        background_image="/grid.png",
        background_repeat="no-repeat",
        background_position="top",
    )
