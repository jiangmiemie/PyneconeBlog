import pynecone as pc
from blog import constants, styles

footer_item_style = {
    "font_family": "Inter",
    "font_weight": "500",
    "_hover": {"color": styles.ACCENT_COLOR},
}

footer_style = {
    "box_shadow": "medium-lg",
    "border_top": "0.2em solid #F0F0F0",
    "vertical_align": "bottom",
    "padding_top": "1em",
    "padding_bottom": "1em",
    "padding_x": styles.PADDING_X2,
}


def footer(style=footer_style):
    return pc.box(
        pc.hstack(
            pc.vstack(
                pc.text("联系我", font_size=styles.H4_FONT_SIZE, font_weight=800),
                pc.link(
                    "GitHub",
                    href=constants.GITHUB_URL,
                    style=footer_item_style,
                ),
                pc.link(
                    "Email",
                    href=constants.CONTACT_URL,
                    style=footer_item_style,
                ),
                align_items="start",
            ),
            pc.vstack(
                pc.text("鸣谢", font_size=styles.H4_FONT_SIZE, font_weight=800),
                pc.link(
                    "Pynecone",
                    href="https://pynecone.io/",
                    style=footer_item_style,
                ),
                pc.link(
                    "React",
                    href="https://react.dev/",
                    style=footer_item_style,
                ),
                align_items="start",
            ),
            pc.vstack(
                pc.text("支持我", font_size=styles.H4_FONT_SIZE, font_weight=800),
                pc.popover(
                    pc.popover_trigger(
                        pc.text("微信"),
                    ),
                    pc.popover_content(pc.popover_body(pc.image(src="/wepay.jpg"))),
                ),
                pc.popover(
                    pc.popover_trigger(
                        pc.text("支付宝"),
                    ),
                    pc.popover_content(pc.popover_body(pc.image(src="/Alipay.jpg"))),
                ),
                align_items="start",
            ),
            justify="space-between",
            color=styles.LIGHT_TEXT_COLOR,
            align_items="top",
            padding_bottom="1em",
            min_width="100%",
        ),
        pc.box(
            frameborder="no",
            border="0",
            marginwidth="0",
            marginheight="0",
            width="100%",
            src=constants.MUSIC_URL,
            element="iframe",
        ),
        **style,
    )
