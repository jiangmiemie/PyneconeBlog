import os
import openai
import pynecone as pc
from dotenv import load_dotenv
from blog.base_state import State as BS
from blog.templates.page import openaipage
from blog.constants import MAIN_URL

load_dotenv()
OPENAIKEY = os.getenv("OPENAIKEY")
openai.api_key = OPENAIKEY


class DalleState(BS):
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


def openainavbar():
    return pc.box(
        pc.hstack(
            pc.link(
                pc.text("GPT"),
                href=f"{MAIN_URL}/openai/chatgpt",
            ),
            pc.link(
                pc.text("DALLE"),
                href=f"{MAIN_URL}/openai/dalle",
            ),
            pc.button(
                pc.icon(tag="moon"),
                on_click=pc.toggle_color_mode,
            ),
            justify="space-evenly",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        border_bottom="1px solid #fff3",
        position="sticky",
        top="0",
        z_index="100",
    )


@openaipage()
def dalle():
    return pc.vstack(
        openainavbar(),
        pc.center(
            pc.vstack(
                pc.heading("DALL-E", font_size="1.5em"),
                pc.input(placeholder="Enter a prompt..", on_blur=DalleState.set_prompt),
                pc.button(
                    "Generate Image",
                    on_click=[DalleState.process_image, DalleState.get_image],
                    width="100%",
                ),
                pc.divider(),
                pc.cond(
                    DalleState.image_processing,
                    pc.circular_progress(is_indeterminate=True),
                    pc.cond(
                        DalleState.image_made,
                        pc.image(
                            src=DalleState.image_url,
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
        ),
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        justify_content="space-between",
    )
