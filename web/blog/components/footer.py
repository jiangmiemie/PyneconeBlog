import pynecone as pc
from blog import constants, styles

footer_item_style = {
    "font_family": "Inter",
    "font_weight": "500",
    "_hover": {"color": styles.ACCENT_COLOR},
}

footer_style = {
    "box_shadow": "medium-lg",
    "border_top": "0.05em solid rgba(100, 116, 139, .2)",
    "vertical_align": "bottom",
    "padding_top": "1em",
    "padding_bottom": "1em",
    "padding_x": styles.PADDING_X2,
}


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
