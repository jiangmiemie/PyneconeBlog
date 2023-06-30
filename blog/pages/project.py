import pynecone as pc
from blog import constants, styles
from blog.templates.page import webpage


difficulty_colors = {"Blog": "green", "Spider": "orange", "project": "blue"}
example_list = [
    {
        "name": "Blog",
        "difficulty": "Blog",
        "tags": ["全栈"],
        "description": "personal web site",
        "img": "/2023/blog.png",
        "source": "https://github.com/jiangmiemie/PyneconeBlog",
        "url": constants.MAIN_URL,
    },
    {
        "name": "halo-theme-2020",
        "difficulty": "Blog",
        "tags": ["前端", "halo"],
        "description": "halo1.5.5 theme",
        "img": "/2023/halo-theme-2020.png",
        "url": "",
        "source": "https://github.com/jiangmiemie/halo-theme-2020",
    },
    {
        "name": "LianJia",
        "difficulty": "Spider",
        "tags": ["爬虫", "代理IP", "多账号"],
        "description": "2023 spider lianjia",
        "img": "/2023/LianJia.png",
        "source": "",
        "url": "{}s/2KCJ".format(constants.SPACE_URL),
    },
    {
        "name": "kickstarter",
        "difficulty": "Spider",
        "tags": ["爬虫", "反爬", "分布式", "故障监测"],
        "description": "2023 spider kickstarter",
        "img": "/2023/kickstarter.png",
        "source": "",
        "url": "{}s/3MFJ".format(constants.SPACE_URL),
    },
    {
        "name": "Yueji",
        "difficulty": "project",
        "tags": ["通用爬虫", "故障监测", "AI"],
        "description": "AI spider",
        "img": "/2023/yueji.png",
        "source": "",
        "url": "https://www.chinashiyue.cn/templates/product3.html",
    },
    {
        "name": "Vulncapture",
        "difficulty": "project",
        "tags": ["模块", "截图"],
        "description": "Auto capture ",
        "img": "/2023/vulncapture.png",
        "source": "https://github.com/jiangmiemie/Vulncapture",
        "url": "https://pypi.org/2023/Vulncapture/",
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


def component_grid():
    sidebar = []
    for category in example_list:
        sidebar.append(
            pc.vstack(
                pc.box(
                    height="10em",
                    background_image=category["img"],
                    background_size="cover",
                    background_position="center",
                    background_repeat="no-repeat",
                    _hover={
                        "background_size": "cover",
                    },
                    rounded="lg",
                ),
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
                    color=styles.DOC_REG_TEXT_COLOR,
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
    return pc.box(pc.responsive_grid(*sidebar, columns=[1, None, 5], spacing="1em"))


@webpage()
def project():
    return pc.box(
        pc.text("记录一些自己做的项目"),
        pc.divider(),
        component_grid(),
        text_align="left",
        margin_bottom="4em",
        padding="4em 4em",
    )
