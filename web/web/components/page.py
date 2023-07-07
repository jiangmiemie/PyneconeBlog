from typing import Callable
import pynecone as pc
from web.base_state import Route, get_path
from web.components.footer import footer
from web.components.navbar import navbar


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
