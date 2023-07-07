import pynecone as pc
from web import constants, styles
from web.base_state import State


class NavbarState(State):
    sidebar_open: bool = False

    def toggle_sidebar(self):
        """Toggle the sidebar open state."""
        self.sidebar_open = not self.sidebar_open


button_style = {
    "_hover": {"color": styles.ACCENT_COLOR, "text_decoration": "none"},
}


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


def navbar(index=False) -> pc.Component:
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
                            "color": styles.ACCENT_COLOR,
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
                                    "color": styles.ACCENT_COLOR,
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
