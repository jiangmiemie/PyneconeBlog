import pynecone as pc
from blog.openai.chat import State

text_light_color = "#fff"
bg_dark_color = "#111"
accennt_light = "#6649D8"
accent_color = "#5535d4"
accent_dark = "#4c2db3"

icon_style = dict(
    font_size="md",
    _hover=dict(color=text_light_color),
    cursor="pointer",
    w="8",
)

sidebar_style = dict(
    border="double 1px transparent;",
    border_radius="10px;",
    background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark});",
    background_origin="border-box;",
    background_clip="padding-box, border-box;",
    p="2",
    _hover=dict(
        background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accennt_light});",
    ),
)


def navbar():
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                pc.link(
                    pc.box(
                        pc.image(src="openai.png", width=30, height="auto"),
                        p="1",
                        border_radius="6",
                        bg="#F0F0F0",
                        mr="2",
                    ),
                    href="/",
                ),
                pc.breadcrumb(
                    pc.breadcrumb_item(
                        pc.heading("GPT", size="sm"),
                    ),
                    pc.breadcrumb_item(
                        pc.text(State.current_chat, size="sm", font_weight="normal"),
                    ),
                ),
            ),
            justify="space-between",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        border_bottom="1px solid #fff3",
        position="sticky",
        top="0",
        z_index="100",
    )


def modal() -> pc.Component:
    """A modal to create a new chat."""
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header(
                    pc.hstack(
                        pc.text("Create new chat"),
                        pc.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                pc.modal_body(
                    pc.input(
                        placeholder="Type something...",
                        on_blur=State.set_new_chat_name,
                        bg="#222",
                        border_color="#fff3",
                        _placeholder={"color": "#fffa"},
                    ),
                ),
                pc.modal_footer(
                    pc.button(
                        "Create",
                        bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#4c2db3"},
                        on_click=[State.create_chat, State.toggle_modal],
                    ),
                ),
                bg="#222",
                color="#fff",
            ),
        ),
        is_open=State.modal_open,
    )


def sidebar_chat(chat: str) -> pc.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return pc.hstack(
        pc.box(
            chat,
            on_click=lambda: State.set_chat(chat),
            style=sidebar_style,
            flex="1",
        ),
        pc.box(
            pc.icon(
                tag="delete",
                style=icon_style,
                on_click=State.delete_chat,
            ),
            style=sidebar_style,
        ),
        color=text_light_color,
        cursor="pointer",
    )


def sidebar() -> pc.Component:
    """The sidebar component."""
    return pc.drawer(
        pc.drawer_overlay(
            pc.drawer_content(
                pc.drawer_header(
                    pc.hstack(
                        pc.button(
                            "+ New chat",
                            px="4",
                            py="2",
                            h="auto",
                            on_click=State.toggle_modal,
                        ),
                        pc.icon(
                            tag="close",
                            on_click=State.toggle_drawer,
                            style=icon_style,
                        ),
                        justify="space-between",
                    )
                ),
                pc.drawer_body(
                    pc.vstack(
                        pc.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
                        align_items="stretch",
                    )
                ),
            ),
        ),
        placement="left",
        is_open=State.drawer_open,
    )
