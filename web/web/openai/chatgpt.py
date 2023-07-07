import os
import openai
import pynecone as pc
from dotenv import load_dotenv
from web.base_state import State as BS
from web.components.page import webpage
from web.constants import MAIN_URL

load_dotenv()
OPENAIKEY = os.getenv("OPENAIKEY")
openai.api_key = OPENAIKEY


class QA(pc.Base):
    """A question and answer pair."""

    question: str
    answer: str


class GPTState(BS):
    chats: list[QA] = [QA(question="What is your name?", answer="Openai")]

    question: str

    async def process_question(self, form_data: dict[str, str]):
        self.question = form_data["question"]
        if self.chats[-1].question == self.question or self.question == "":
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
        self.chats.append(qa)

        for item in session:
            answer_text = item["choices"][0]["text"]
            self.chats[-1].answer += answer_text
            self.chats = self.chats
            yield


def message(qa: QA) -> pc.Component:
    return pc.box(
        pc.box(
            pc.box(
                pc.markdown(qa.question),
                bg="#fff3",
                shadow="rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;",
                display="inline-block",
                border_radius="xl",
                p="4",
                max_w="30em",
            ),
            text_align="right",
            margin_top="1em",
        ),
        pc.box(
            pc.box(
                pc.markdown(qa.answer),
                color="white",
                bg="#5535d4",
                shadow="rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;",
                display="inline-block",
                border_radius="xl",
                p="4",
                max_w="30em",
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


@webpage()
def chatgpt() -> pc.Component:
    """List all the messages in a single conversation."""
    return pc.vstack(
        pc.vstack(
            pc.box(
                pc.foreach(GPTState.chats, message),
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
        ),
        pc.box(
            pc.vstack(
                pc.form(
                    pc.hstack(
                        pc.input(
                            placeholder="Type something...",
                            on_change=GPTState.set_question,
                            id="question",
                            _hover={"border_color": "#5535d4"},
                        ),
                    ),
                    on_submit=GPTState.process_question,
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
        ),
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        justify_content="space-between",
    )
