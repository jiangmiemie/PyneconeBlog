import reflex as pc
from web import constants
from typing import Callable
from web.base_state import State
from web.base_state import Route, get_path


button_style = {
    "_hover": {"color": constants.ACCENT_COLOR, "text_decoration": "none"},
}

footer_item_style = {
    "font_family": "Inter",
    "font_weight": "500",
    "_hover": {"color": constants.ACCENT_COLOR},
}

footer_style = {
    "box_shadow": "medium-lg",
    "border_top": "0.05em solid rgba(100, 116, 139, .2)",
    "vertical_align": "bottom",
    "padding_top": "1em",
    "padding_bottom": "1em",
    "padding_x": constants.PADDING_X2,
}


class NavbarState(State):
    sidebar_open: bool = False

    def toggle_sidebar(self):
        """Toggle the sidebar open state."""
        self.sidebar_open = not self.sidebar_open


def navbar(index=False) -> pc.Component:
    def get_sidebar(align, index=False):
        index_links = pc.link(
            pc.text(
                "首页",
                _focus={},
            ),
            **button_style,
            href=constants.MAIN_URL,
        )

        return align(
            pc.link(
                pc.text(
                    "开往",
                ),
                href="https://www.travellings.cn/go.html",
                **button_style,
            ),
            index_links if index == False else pc.box(),
        )

    sidebarh = get_sidebar(pc.hstack, index)
    sidebarv = get_sidebar(pc.vstack, index)
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.desktop_only(
                    pc.hstack(
                        sidebarh,
                        spacing="1.5em",
                    )
                ),
                pc.mobile_and_tablet(
                    pc.icon(
                        tag="hamburger",
                        on_click=NavbarState.toggle_sidebar,
                        width="1.5em",
                        height="1.5em",
                        _hover={
                            "cursor": "pointer",
                            "color": constants.ACCENT_COLOR,
                        },
                    ),
                ),
                spacing="1em",
            ),
            pc.hstack(
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
                            pc.icon(
                                tag="close",
                                on_click=NavbarState.toggle_sidebar,
                                width="4em",
                                _hover={
                                    "cursor": "pointer",
                                    "color": constants.ACCENT_COLOR,
                                },
                            ),
                            justify="space-between",
                            margin_bottom="1.5em",
                        ),
                        sidebarv,
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
            padding_x=constants.PADDING_X,
        ),
        backdrop_filter="blur(10px)",
        padding_y=["0.8em", "0.8em", "0.5em"],
        border_bottom="0.05em solid rgba(100, 116, 139, .2)",
        position="sticky",
        width="100%",
        top="0px",
        z_index="99",
    )


def footer(style=footer_style):
    return pc.box(
        pc.hstack(
            pc.vstack(
                pc.link(
                    pc.span("CC BY-NC-SA 4.0", font_weight="bold"),
                    href="https://creativecommons.org/licenses/by-nc-sa/4.0/",
                ),
                pc.span(" 2021 年至今 © jiangmiemie"),
                align_items="left",
            ),
            pc.hstack(
                pc.link(
                    pc.image(
                        src="/github.png",
                        width="40px",
                        height="auto",
                    ),
                    href=constants.GITHUB_URL,
                    style=footer_item_style,
                ),
                pc.link(
                    pc.image(
                        src="/discord.png",
                        width="40px",
                        height="auto",
                    ),
                    href="https://discordapp.com/users/jiangyangcreate#0902",
                    style=footer_item_style,
                ),
                spacing="2em",
            ),
            justify="space-between",
        ),
        **style,
    )


def webpage(
    path: str | None = None,
    title: str | None = None,
    index=False,
) -> Callable:
    def webpage(
        contents: Callable[[], Route], path=path, title=title, index=index
    ) -> Route:
        if path is None:
            path = get_path(contents)
        else:
            path = path
        if title is None:
            title = f"{contents.__name__.replace('_', ' ').title()} | Islands"
        else:
            title = title

        def wrapper() -> pc.Component:
            return pc.box(
                navbar(index),
                contents(),
                footer(),
                font_family="Inter",
            )

        return Route(
            path=path,
            title=title,
            component=wrapper,
        )

    return webpage
