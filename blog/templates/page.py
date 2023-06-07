"""Template for documentation pages."""
from typing import Callable
import pynecone as pc
from blog import styles
from blog import constants
from blog.route import Route, get_path


link_style = {
    "color": styles.LIGHT_TEXT_COLOR,
    "font_weight": "500",
    "_hover": {"color": styles.ACCENT_COLOR},
    "fontSize": "1.2em",
}


def docheader(
    text: str,
    first: bool = False,
    font_size: float = None,
    coming_soon: bool = False,
    divider: bool = True,
    **props,
) -> pc.Component:
    # Get the basic styles.
    style = {"marginTop": "1em"} if not first else {}
    if font_size:
        style["fontSize"] = font_size

    # Set the text.
    children = [pc.heading(text, style=style, **props)]

    # Add a badge if the header is coming soon.
    if coming_soon:
        children.append(
            pc.badge(
                "Coming Soon!",
                bg=styles.ACCENT_COLOR,
                color="white",
            ),
        )

    # Add a divider if needed.
    if divider:
        children.append(pc.divider())

    # Return the header.
    return pc.box(
        *children,
        id="-".join(text.lower().split()),
        # color=styles.DOC_HEADER_COLOR,
        font_weight=styles.DOC_HEADING_FONT_WEIGHT,
        width="100%",
    )


def doctext(*text, **props) -> pc.Component:
    """Create a documentation paragraph.

    Args:
        text: The text components to display.
        props: Props to apply to the paragraph.

    Returns:
        The styled paragraph.
    """
    return pc.box(
        *text,
        margin_bottom="1em",
        font_size=styles.TEXT_FONT_SIZE,
        width="100%",
        **props,
    )


def imgpage(set_path: str | None = None, t: str | None = None) -> pc.Component:
    def imgpage(contents: Callable[[], Route]) -> Route:
        if set_path is None:
            path = get_path(contents)
        else:
            path = set_path

        # Set the page title.
        if t is None:
            title = f"{contents.__name__.replace('_', ' ').title()} | Islands"
        else:
            title = t

        def wrapper(*args, **kwargs) -> pc.Component:
            from blog.components.footer import footer
            from blog.components.navbar import navbar

            if not isinstance(contents, pc.Component):
                comp = contents(*args, **kwargs)
            else:
                comp = contents

            return pc.box(
                navbar(),
                pc.box(
                    pc.flex(
                        pc.vstack(
                            pc.box(comp),
                            padding_left=["1em", "2em", "5em", "8em"],
                            padding_right=styles.PADDING_X,
                            width=["100%", "100%", "100%", "100%"],
                            padding_top="2em",
                        ),
                        max_width="80em",
                        margin_x="auto",
                        margin_top="1em",
                    ),
                    footer(),
                    font_family="Inter",
                ),
            )

        # Return the route.
        return Route(
            path=path,
            title=title,
            component=wrapper,
        )

    return imgpage


def mdpage(text: str, path: str, title: str, time: str, *args, **kwargs):
    from blog.components.footer import footer
    from blog.components.navbar import navbar
    from blog.components.sidebar import get_prev_next

    prev, next = get_prev_next(path)

    links = []

    if prev:
        links.append(
            pc.link(
                "← " + prev.title,
                href=prev.path,
                style=link_style,
            )
        )
    else:
        links.append(pc.box())

    if next:
        links.append(
            pc.link(
                next.title + " →",
                href=next.path,
                style=link_style,
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
        pc.box(
            pc.box(id="contentslist"),
            pc.flex(
                pc.vstack(
                    pc.box(
                        comp,
                        pc.divider(),
                        doctext(
                            "本文最后修改于{}年{}月".format(str(time)[:4], int(str(time)[4:]))
                        ),
                        pc.alert(
                            pc.alert_icon(),
                            pc.alert_title(
                                pc.markdown(
                                    "版权声明 © : 采用 [**知识共享署名4.0**](https://creativecommons.org/licenses/by/4.0/legalcode) 国际许可协议进行许可 , 转载请注明出处！"
                                )
                            ),
                            status="info",
                        ),
                        id="contents",
                    ),
                    pc.flex(
                        *links,
                        justify="space-between",
                        width="100%",
                        padding_top="1em",
                        padding_bottom="1em",
                    ),
                ),
                padding_left=["1em", "2em", "5em", "8em"],
                padding_right=styles.PADDING_X,
                width=["100%", "100%", "100%", "95%"],
                padding_top="2em",
            ),
            max_width="80em",
            margin_x="auto",
            margin_top="1em",
        ),
        footer(),
        font_family="Inter",
    )


def webpage(path: str, title: str = constants.DEFAULT_TITLE, props=None) -> Callable:
    props = props or {}

    def webpage(contents: Callable[[], Route]) -> Route:
        """Wrapper to create a templated route.

        Args:
            contents: The function to create the page route.

        Returns:
            The templated route.
        """

        def wrapper(*children, **props) -> pc.Component:
            """The template component.

            Args:
                children: The children components.
                props: The props to apply to the component.

            Returns:
                The component with the template applied.
            """
            # Import here to avoid circular imports.
            from blog.components.footer import footer
            from blog.components.navbar import navbar_index

            # Wrap the component in the template.
            return pc.box(
                navbar_index(),
                contents(*children, **props),
                footer(),
                font_family="Inter",
                **props,
            )

        return Route(
            path=path,
            title=title,
            component=wrapper,
        )

    return webpage
