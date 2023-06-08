import pynecone as pc
from blog import constants, styles
from blog.base_state import State
from blog.pages.index import index
from blog.tsclient import client


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
                color=styles.DOC_HEADER_COLOR,
            ),
            pc.divider(),
            pc.text(
                result["document"]["description"],
                font_weight=400,
                color=styles.DOC_REG_TEXT_COLOR,
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


button_style = {
    "_hover": {"color": styles.ACCENT_COLOR, "text_decoration": "none"},
}


def get_sidebar():
    return pc.vstack(
        pc.link(
            pc.text(
                "月记",
            ),
            href="/month",
            **button_style,
        ),
        pc.link(
            pc.text(
                "相册",
            ),
            href="/gallery",
            **button_style,
        ),
        pc.link(
            pc.text(
                "读书",
            ),
            href="/read",
            **button_style,
        ),
        pc.link(
            pc.text(
                "编程",
            ),
            href="/code",
            **button_style,
        ),
        pc.menu(
            pc.menu_button(
                "关于",
                **button_style,
            ),
            pc.menu_list(
                pc.link(
                    pc.menu_item(
                        "原则",
                        _hover={"background_color": "white"},
                        _focus={},
                    ),
                    **button_style,
                    href="/principle",
                ),
                pc.link(
                    pc.menu_item("项目经历", _hover={"background_color": "white"}),
                    **button_style,
                    href="/project",
                ),
                pc.menu_divider(),
                pc.link(
                    pc.menu_item(
                        "我的云盘",
                        _hover={"background_color": "white"},
                        _focus={},
                    ),
                    **button_style,
                    href=constants.SPACE_URL,
                ),
            ),
        ),
    )


def navbar_index(sidebar: pc.Component = get_sidebar()) -> pc.Component:
    # Create the navbar component.
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.desktop_only(
                    pc.hstack(
                        pc.link(
                            pc.text(
                                "月记",
                            ),
                            href="/month",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "相册",
                            ),
                            href="/gallery",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "读书",
                            ),
                            href="/read",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "编程",
                            ),
                            href="/code",
                            **button_style,
                        ),
                        pc.menu(
                            pc.menu_button(
                                "关于",
                                pc.icon(tag="chevron_down"),
                                color=styles.DOC_REG_TEXT_COLOR,
                                **button_style,
                            ),
                            pc.menu_list(
                                pc.link(
                                    pc.menu_item(
                                        "原则",
                                        _hover={"background_color": "white"},
                                        _focus={},
                                    ),
                                    **button_style,
                                    href="/principle",
                                ),
                                pc.link(
                                    pc.menu_item(
                                        "项目经历", _hover={"background_color": "white"}
                                    ),
                                    **button_style,
                                    href="/project",
                                ),
                                pc.menu_divider(),  # 下拉标签分组
                                pc.link(
                                    pc.menu_item(
                                        "我的云盘",
                                        _hover={"background_color": "white"},
                                        _focus={},
                                    ),
                                    **button_style,
                                    href=constants.SPACE_URL,
                                ),
                            ),
                        ),
                    ),
                ),
                pc.mobile_and_tablet(
                    pc.icon(
                        tag="hamburger",
                        on_click=NavbarState.toggle_sidebar,
                        width="1.5em",
                        height="1.5em",
                        _hover={
                            "cursor": "pointer",
                            "color": styles.ACCENT_COLOR,
                        },
                    ),
                ),
                spacing="1em",
            ),
            pc.hstack(
                pc.link(
                    pc.text(
                        "开往",
                    ),
                    href="https://www.travellings.cn/go.html",
                    **button_style,
                ),
                pc.button(
                    pc.icon(tag="moon"),
                    on_click=pc.toggle_color_mode,
                ),
                _hover={"text_decoration": "none"},
                spacing="1em",
            ),
            pc.drawer(
                pc.drawer_overlay(
                    pc.drawer_content(
                        pc.hstack(
                            pc.hstack(
                                pc.input_group(
                                    pc.input_left_addon(
                                        pc.icon(
                                            tag="search",
                                            color=styles.DOC_REG_TEXT_COLOR,
                                        ),
                                        bg="rgba(255,255,255, 0.8)",
                                        backdrop_filter="blur(10px)",
                                        on_click=NavbarState.change_search,
                                    ),
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
                            ),
                            pc.icon(
                                tag="close",
                                on_click=NavbarState.toggle_sidebar,
                                width="4em",
                                _hover={
                                    "cursor": "pointer",
                                    "color": styles.ACCENT_COLOR,
                                },
                            ),
                            justify="space-between",
                            margin_bottom="1.5em",
                        ),
                        sidebar,
                        padding_x="2em",
                        padding_top="2em",
                    ),
                ),
                position="fixed",
                left="0px",
                placement="left",
                auto_focus=False,
                block_scroll_on_mount=False,
                is_open=NavbarState.sidebar_open,
                on_close=NavbarState.toggle_sidebar,
            ),
            pc.modal(
                pc.modal_overlay(
                    pc.modal_content(
                        pc.modal_body(
                            pc.vstack(
                                pc.vstack(
                                    pc.foreach(
                                        NavbarState.search_results,
                                        format_search_results,
                                    ),
                                    spacing="0.5em",
                                    width="100%",
                                    max_height="30em",
                                    align_items="start",
                                    overflow="auto",
                                ),
                            ),
                            opacity=0.8,
                        ),
                        opacity=0.1,
                    )
                ),
                is_open=NavbarState.search_modal,
                on_close=NavbarState.change_search,
                padding="1em",
            ),
            justify="space-between",
            padding_x=styles.PADDING_X,
        ),
        backdrop_filter="blur(10px)",
        padding_y=["0.8em", "0.8em", "0.5em"],
        border_bottom="0.05em solid rgba(100, 116, 139, .2)",
        position="sticky",
        width="100%",
        top="0px",
        z_index="99",
    )


def navbar(sidebar: pc.Component = get_sidebar()) -> pc.Component:
    # Create the navbar component.
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.button(
                    pc.icon(tag="moon"),
                    on_click=pc.toggle_color_mode,
                ),
                pc.link(
                    pc.text(
                        "欢迎回来",
                        font_size=styles.H3_FONT_SIZE,
                        font_weight=600,
                    ),
                    href=index.path,
                    spacing="0.25em",
                ),
                _hover={"text_decoration": "none"},
                spacing="1em",
            ),
            pc.desktop_only(
                pc.hstack(
                    pc.input_group(
                        pc.input_left_addon(
                            pc.icon(tag="search", color=styles.DOC_REG_TEXT_COLOR),
                            bg="rgba(255,255,255, 0.8)",
                            backdrop_filter="blur(10px)",
                            on_click=NavbarState.change_search,
                        ),
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
                ),
            ),
            pc.hstack(
                pc.desktop_only(
                    pc.hstack(
                        pc.link(
                            pc.text(
                                "月记",
                            ),
                            href="/month",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "相册",
                            ),
                            href="/gallery",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "读书",
                            ),
                            href="/read",
                            **button_style,
                        ),
                        pc.link(
                            pc.text(
                                "编程",
                            ),
                            href="/code",
                            **button_style,
                        ),
                        pc.menu(
                            pc.menu_button(
                                "关于",
                                pc.icon(tag="chevron_down"),
                                color=styles.DOC_REG_TEXT_COLOR,
                                **button_style,
                            ),
                            pc.menu_list(
                                pc.link(
                                    pc.menu_item(
                                        "原则",
                                        _hover={"background_color": "white"},
                                        _focus={},
                                    ),
                                    **button_style,
                                    href="/principle",
                                ),
                                pc.link(
                                    pc.menu_item(
                                        "项目经历", _hover={"background_color": "white"}
                                    ),
                                    **button_style,
                                    href="/project",
                                ),
                                pc.menu_divider(),  # 下拉标签分组
                                pc.link(
                                    pc.menu_item(
                                        "我的云盘",
                                        _hover={"background_color": "white"},
                                        _focus={},
                                    ),
                                    **button_style,
                                    href=constants.SPACE_URL,
                                ),
                            ),
                        ),
                    ),
                ),
                pc.link(
                    pc.text(
                        "开往",
                    ),
                    href="https://www.travellings.cn/go.html",
                    **button_style,
                ),
                pc.mobile_and_tablet(
                    pc.icon(
                        tag="hamburger",
                        on_click=NavbarState.toggle_sidebar,
                        width="1.5em",
                        height="1.5em",
                        _hover={
                            "cursor": "pointer",
                            "color": styles.ACCENT_COLOR,
                        },
                    ),
                ),
                spacing="1em",
            ),
            pc.modal(
                pc.modal_overlay(
                    pc.modal_content(
                        pc.modal_body(
                            pc.vstack(
                                pc.vstack(
                                    pc.foreach(
                                        NavbarState.search_results,
                                        format_search_results,
                                    ),
                                    spacing="0.5em",
                                    width="100%",
                                    max_height="30em",
                                    align_items="start",
                                    overflow="auto",
                                ),
                            ),
                            opacity=0.8,
                        ),
                        opacity=0.1,
                    )
                ),
                is_open=NavbarState.search_modal,
                on_close=NavbarState.change_search,
                padding="1em",
            ),
            pc.drawer(
                pc.drawer_overlay(
                    pc.drawer_content(
                        pc.hstack(
                            pc.hstack(
                                pc.input_group(
                                    pc.input_left_addon(
                                        pc.icon(
                                            tag="search",
                                            color=styles.DOC_REG_TEXT_COLOR,
                                        ),
                                        bg="rgba(255,255,255, 0.8)",
                                        backdrop_filter="blur(10px)",
                                        on_click=NavbarState.change_search,
                                    ),
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
                            ),
                            pc.icon(
                                tag="close",
                                on_click=NavbarState.toggle_sidebar,
                                width="4em",
                                _hover={
                                    "cursor": "pointer",
                                    "color": styles.ACCENT_COLOR,
                                },
                            ),
                            justify="space-between",
                            margin_bottom="1.5em",
                        ),
                        sidebar,
                        padding_x="2em",
                        padding_top="2em",
                    ),
                ),
                position="fixed",
                left="0px",
                placement="left",
                auto_focus=False,
                block_scroll_on_mount=False,
                is_open=NavbarState.sidebar_open,
                on_close=NavbarState.toggle_sidebar,
            ),
            justify="space-between",
            padding_x=styles.PADDING_X,
        ),
        backdrop_filter="blur(10px)",
        padding_y=["0.8em", "0.8em", "0.5em"],
        border_bottom="0.05em solid rgba(100, 116, 139, .2)",
        position="sticky",
        width="100%",
        top="0px",
        z_index="99",
    )
