import pynecone as pc
import openai
import os
from dotenv import load_dotenv
from blog.base_state import State as BS

load_dotenv()
OPENAIKEY = os.getenv("OPENAIKEY")
openai.api_key = OPENAIKEY


shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
message_style = dict(display="inline-block", border_radius="xl", p="4", max_w="30em")
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


class QA(pc.Base):
    """A question and answer pair."""

    question: str
    answer: str


class State(BS):
    """The dalle state."""

    prompt = ""
    image_url = ""
    image_processing = False
    image_made = False

    def process_image(self):
        """Set the image processing flag to true and indicate that the image has not been made yet."""
        self.image_made = False
        self.image_processing = True

    def get_image(self):
        """Get the image from the prompt."""
        try:
            response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
            self.image_url = response["data"][0]["url"]
            # Set the image processing flag to false and indicate that the image has been made.
            self.image_processing = False
            self.image_made = True
        except:
            self.image_processing = False
            return pc.window_alert("Error with OpenAI Execution.")

    """The chat state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = {
        "Intros": [QA(question="What is your name?", answer="Openai")],
    }

    # The current chat name.
    current_chat = "Intros"

    # The currrent question.
    question: str

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    def create_chat(self):
        """Create a new chat."""
        # Insert a default question.
        self.chats[self.new_chat_name] = [
            QA(question="What is your name?", answer="Openai")
        ]
        self.current_chat = self.new_chat_name

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = {
                "New Chat": [QA(question="What is your name?", answer="Openai")]
            }
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @pc.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Check if we have already asked the last question or if the question is empty
        self.question = form_data["question"]
        if (
            self.chats[self.current_chat][-1].question == self.question
            or self.question == ""
        ):
            return

        session = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.question,
            max_tokens=3200,
            n=1,
            stop=None,
            temperature=0.7,
            stream=True,  # Enable streaming
        )
        qa = QA(question=self.question, answer="")
        self.chats[self.current_chat].append(qa)

        for item in session:
            answer_text = item["choices"][0]["text"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield


def message(qa: QA) -> pc.Component:
    return pc.box(
        pc.box(
            pc.box(
                pc.markdown(qa.question),
                bg="#fff3",
                shadow=shadow_light,
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        pc.box(
            pc.box(
                pc.markdown(qa.answer),
                color="white",
                bg="#5535d4",
                shadow=shadow_light,
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> pc.Component:
    """List all the messages in a single conversation."""
    return pc.vstack(
        pc.box(
            pc.foreach(State.chats[State.current_chat], message),
            width="100%",
        ),
        py="8",
        flex="1",
        width="100%",
        max_w="3xl",
        padding_x="4",
        align_self="center",
        align_items="stretch",
        overflow="hidden",
        padding_bottom="5em",
        justify_content="space-between",
        border="5px  #555",
        box_shadow="lg",
    )


def action_bar() -> pc.Component:
    """The action bar to send a new message."""
    return pc.box(
        pc.vstack(
            pc.form(
                pc.hstack(
                    pc.input(
                        placeholder="Type something...",
                        on_change=State.set_question,
                        id="question",
                        _hover={"border_color": "#5535d4"},
                    ),
                ),
                on_submit=State.process_question,
                width="100%",
            ),
            pc.text(
                "thanks for pynecone and openai(text-davinci-003) Please be careful not to keep asking the same question",
                font_size="xs",
                text_align="center",
            ),
            width="100%",
            max_w="3xl",
            mx="auto",
            align_items="stretch",
            justify_content="space-between",
        ),
        padding_x="2em",
        border="5px  #555",
        box_shadow="lg",
        position="sticky",
        bottom="0",
        left="0",
        py="4",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid #fff3",
        align_items="stretch",
        width="100%",
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
            pc.button(
                pc.icon(tag="moon"),
                on_click=pc.toggle_color_mode,
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


def chatgpt() -> pc.Component:
    """The main app."""
    return pc.vstack(
        navbar(),
        chat(),
        action_bar(),
        sidebar(),
        modal(),
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        justify_content="space-between",
    )


def dalle():
    return pc.center(
        pc.vstack(
            pc.heading("DALL-E", font_size="1.5em"),
            pc.input(placeholder="Enter a prompt..", on_blur=State.set_prompt),
            pc.button(
                "Generate Image",
                on_click=[State.process_image, State.get_image],
                width="100%",
            ),
            pc.divider(),
            pc.cond(
                State.image_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    State.image_made,
                    pc.image(
                        src=State.image_url,
                        height="25em",
                        width="25em",
                    ),
                ),
            ),
            bg="white",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )
