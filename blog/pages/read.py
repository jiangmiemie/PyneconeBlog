import pynecone as pc
from blog.templates.page import imgpage, docheader, doctext
from blog import tsclient


def component_grid():
    sidebar = []
    pagelists = tsclient.check_data_by_tag("read")
    for pagelist in pagelists:
        sidebar.insert(
            0,
            pc.link(
                pc.vstack(
                    pc.heading(pagelist.title, style={"fontSize": "1.2em"}),
                    align_items="left",
                    row_span=3,
                    col_span=1,
                    box_shadow="lg",
                    border_radius="1em",
                    padding="1em",
                    _hover={
                        "box_shadow": "rgba(38, 57, 77, .3) 0px 20px 30px -10px",
                    },
                ),
                href=pagelist.path,
            ),
        )
    return pc.box(
        pc.responsive_grid(*sidebar, columns=[2, 3, 4, 5, 7], gap=4),
    )


@imgpage()
def read():
    return pc.flex(
        pc.hstack(
            pc.box(
                docheader("相册", first=True),
                doctext("记录了一些生活的片段"),
                pc.divider(),
                component_grid(),
                text_align="left",
            ),
            align_items="start",
        ),
        flex_direction="column",
        height="100%",
        margin_bottom="4em",
    )
