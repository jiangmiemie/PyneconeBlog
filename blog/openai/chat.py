import pynecone as pc
import openai
from blog.key import openaikey
from blog.base_state import State as BS

openai.api_key = openaikey


shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
message_style = dict(display="inline-block", border_radius="xl", p="4", max_w="30em")


class QA(pc.Base):
    """A question and answer pair."""

    question: str
    answer: str


class State(BS):
    """The app state."""

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
