import inspect
from typing import Callable
import pynecone as pc
from pynecone.base import Base


class State(pc.State):
    """The base state."""


class CloseSidebarMiddleware(pc.Middleware):
    def preprocess(self, app, state, event):
        if event.name == pc.event.get_hydrate_event(state):
            state.get_substate(["navbar_state"]).sidebar_open = False


class Route(Base):
    """A page route."""

    # The path of the route.
    path: str

    # The page title.
    title: str | None = None

    # The component to render for the route.
    component: pc.Component | Callable[[], pc.Component]


def get_path(component_fn: Callable):
    """Get the path for a page based on the file location.

    Args:
        component_fn: The component function for the page.
    """
    module = inspect.getmodule(component_fn)

    # Create a path based on the module name.
    return (
        module.__name__.replace(".", "/")
        .replace("_", "-")
        .replace("blog/", "")
        .replace("pages", "")
    )
