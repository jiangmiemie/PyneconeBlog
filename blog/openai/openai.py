"""The main Chat app."""

import pynecone as pc
from blog.openai import chat
from blog.openai import modal, navbar, sidebar


def openai() -> pc.Component:
    """The main app."""
    return pc.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        justify_content="space-between",
    )
