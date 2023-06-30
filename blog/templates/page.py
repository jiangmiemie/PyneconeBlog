from typing import Callable
import pynecone as pc
from blog import styles
from blog.base_state import Route, get_path
from blog import tsclient
from blog.components.footer import footer
from blog.components.navbar import navbar


def component_grid(tag):
    sidebar = []
    pagelists = tsclient.check_data(
        sql=f"SELECT * FROM reflexblog WHERE category='{tag}'"
    )
    for pagelist in pagelists:
        sidebar.insert(
            0,
            pc.link(
                pc.box(
                    pc.heading(pagelist[2], style={"fontSize": "1.2em"}),
                    align_items="center",
                    box_shadow="lg",
                    padding="1em",
                    _hover={
                        "box_shadow": "rgba(38, 57, 77, .3) 0px 20px 30px -10px",
                    },
                    background_image="{}.svg".format(tag),
                    background_repeat="no-repeat",
                    background_position="right bottom",
                    background_size="4em",
                ),
                href=pagelist[1],
            ),
        )
    return pc.box(
        pc.responsive_grid(*sidebar, columns=[2, None, 5], spacing="1em"),
        width="100%",
    )


def webpage(
    path: str | None = None, title: str | None = None, index=False, *children, **props
) -> Callable:
    def webpage(
        contents: Callable[[], Route], path=path, title=title, props=props, index=index
    ) -> Route:
        if path is None:
            path = get_path(contents)
        else:
            path = path
        if title is None:
            title = f"{contents.__name__.replace('_', ' ').title()} | Islands"
        else:
            title = title
        if not isinstance(contents, pc.Component):
            comp = contents(*children, **props)
        else:
            comp = contents

        def wrapper(*children, **props) -> pc.Component:
            return pc.box(
                navbar(index),
                pc.box(
                    comp,
                    footer(),
                    width="100%",
                    height="100vh",
                ),
                font_family="Inter",
                **props,
            )

        return Route(
            path=path,
            title=title,
            component=wrapper,
        )

    return webpage


def mdpage(text: str, path: str, title: str, time: str, *args, **kwargs):
    from blog.components.sidebar import get_prev_next

    prev, next = get_prev_next(path)
    links = []
    if prev:
        links.append(
            pc.link(
                "← " + prev.title,
                href=prev.path,
                style={
                    "color": styles.LIGHT_TEXT_COLOR,
                    "font_weight": "500",
                    "_hover": {"color": styles.ACCENT_COLOR},
                    "fontSize": "1.2em",
                },
            )
        )
    else:
        links.append(pc.box())

    if next:
        links.append(
            pc.link(
                next.title + " →",
                href=next.path,
                style={
                    "color": styles.LIGHT_TEXT_COLOR,
                    "font_weight": "500",
                    "_hover": {"color": styles.ACCENT_COLOR},
                    "fontSize": "1.2em",
                },
            )
        )
    else:
        links.append(pc.box())

    contents = pc.markdown(text)

    if not isinstance(contents, pc.Component):
        comp = contents(*args, **kwargs)
    else:
        comp = contents

    return pc.box(
        navbar(),
        pc.center(
            pc.flex(
                pc.vstack(
                    pc.box(id="contentslist"),
                    pc.box(
                        comp,
                        pc.divider(),
                        pc.text(
                            "本文最后修改于{}年{}月".format(str(time)[:4], int(str(time)[4:]))
                        ),
                        pc.alert(
                            pc.alert_icon(),
                            pc.alert_title(
                                pc.markdown(
                                    "版权声明 © : 采用 [**知识共享署名4.0**](https://creativecommons.org/licenses/by/4.0/legalcode) 国际许可协议进行许可 , 转载请注明来源 https://www.jiangmiemie.com/"
                                )
                            ),
                            status="info",
                        ),
                        id="contents",
                        text_align="left",
                    ),
                    pc.flex(
                        *links,
                        justify="space-between",
                        width="100%",
                        padding_top="0.5em",
                        padding_bottom="1em",
                    ),
                ),
                padding_x="2em",
                border="5px  #555",
                box_shadow="lg",
                width=["100%", "100%", "100%", "80%"],
                padding_top="1em",
            ),
            margin_x="auto",
            margin_top="1em",
        ),
        footer(),
        font_family="Inter",
    )
