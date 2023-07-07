import pynecone as pc
from web import constants
from web.page import webpage


difficulty_colors = {"Blog": "green", "Spider": "orange", "project": "blue"}
example_list = [
    {
        "name": "ChatGPT",
        "difficulty": "project",
        "tags": ["全栈"],
        "description": "personal web site",
        "source": "{}/openai/chatgpt".format(constants.GITHUB_PRO_URL),
        "url": "{}/openai/chatgpt".format(constants.MAIN_URL),
    },
    {
        "name": "Dalle",
        "difficulty": "project",
        "tags": ["全栈"],
        "description": "personal web site",
        "source": "{}/openai/chatgpt".format(constants.GITHUB_PRO_URL),
        "url": "{}/openai/dalle".format(constants.MAIN_URL),
    },
    {
        "name": "数据库",
        "difficulty": "project",
        "tags": ["全栈"],
        "description": "personal web site",
        "source": "{}/openai/chatgpt".format(constants.GITHUB_PRO_URL),
        "url": "{}/pgsql/pgsql".format(constants.MAIN_URL),
    },
]


class Gallery(pc.Model):
    name: str
    difficulty: str
    tags: list[str]
    description: str
    img: str
    gif: str
    url: str
    source: str


@webpage(path="/", index=True)
def project():
    sidebar = []
    for category in example_list:
        sidebar.append(
            pc.vstack(
                pc.hstack(
                    pc.spacer(),
                    pc.badge(
                        category["difficulty"],
                        color_scheme=difficulty_colors[category["difficulty"]],
                    ),
                ),
                pc.heading(category["name"], style={"fontSize": "1.2em"}),
                pc.box(
                    category["description"],
                    style={"fontSize": "0.6em"},
                    color=constants.DOC_REG_TEXT_COLOR,
                    height="3.5em",
                ),
                pc.divider(),
                pc.hstack(
                    *[
                        pc.badge(tag, border_radius="15px", padding_x=".5em")
                        for tag in category["tags"]
                    ],
                    padding_bottom=".5em",
                ),
                pc.vstack(
                    pc.link(
                        pc.hstack(pc.text("Source Code"), pc.icon(tag="external_link")),
                        href=category["source"],
                    )
                    if category["source"]
                    else pc.box(),
                    align_items="left",
                ),
                pc.vstack(
                    pc.link(
                        pc.hstack(pc.text("Live"), pc.icon(tag="view")),
                        href=category["url"],
                    )
                    if category["url"]
                    else pc.box(),
                    align_items="left",
                ),
                align_items="left",
                box_shadow="lg",
                border_radius="1em",
                padding="1em",
                _hover={
                    "box_shadow": "rgba(38, 57, 77, .3) 0px 20px 30px -10px",
                },
            )
        )
    return pc.box(
        pc.responsive_grid(*sidebar, columns=[1, None, 5], spacing="1em"),
        padding="6em 4em",
    )
