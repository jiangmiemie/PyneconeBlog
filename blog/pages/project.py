import pynecone as pc
from blog import constants, styles
from blog.templates.page import imgpage, docheader, doctext


difficulty_colors = {"Blog": "green", "Spider": "orange", "project": "blue"}
example_list = [
    {
        "name": "Blog",
        "difficulty": "Blog",
        "tags": ["全栈"],
        "description": "personal web site",
        "img": "/pages/project/blog.png",
        "source": "https://github.com/jiangmiemie/PyneconeBlog",
        "url": constants.MAIN_URL,
    },
    {
        "name": "halo-theme-2020",
        "difficulty": "Blog",
        "tags": ["前端", "halo"],
        "description": "halo1.5.5 theme",
        "img": "/pages/project/halo-theme-2020.png",
        "url": "",
        "source": "https://github.com/jiangmiemie/halo-theme-2020",
    },
    {
        "name": "LianJia",
        "difficulty": "Spider",
        "tags": ["爬虫", "代理IP", "多账号"],
        "description": "2023 spider lianjia",
        "img": "/pages/project/LianJia.png",
        "source": "",
        "url": "{}s/2KCJ".format(constants.SPACE_URL),
    },
    {
        "name": "kickstarter",
        "difficulty": "Spider",
        "tags": ["爬虫", "反爬", "分布式", "故障监测"],
        "description": "2023 spider kickstarter",
        "img": "/pages/project/kickstarter.png",
        "source": "",
        "url": "{}s/3MFJ".format(constants.SPACE_URL),
    },
    {
        "name": "Yueji",
        "difficulty": "project",
        "tags": ["通用爬虫", "故障监测", "AI"],
        "description": "AI spider",
        "img": "/pages/project/yueji.png",
        "source": "",
        "url": "https://www.chinashiyue.cn/templates/product3.html",
    },
    {
        "name": "Vulncapture",
        "difficulty": "project",
        "tags": ["模块", "截图"],
        "description": "Auto capture ",
        "img": "/pages/project/vulncapture.png",
        "source": "https://github.com/jiangmiemie/Vulncapture",
        "url": "https://pypi.org/pages/project/Vulncapture/",
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
                row_span=3,
                col_span=1,
                box_shadow="lg",
                border_radius="1em",
                padding="1em",
                _hover={
                    "box_shadow": "rgba(38, 57, 77, .3) 0px 20px 30px -10px",
                },
            )
        )
    return pc.box(pc.responsive_grid(*sidebar, columns=[1, 2, 2, 4, 5]))


@imgpage()
def project():
    return pc.box(
        docheader("项目", first=True),
        doctext("记录一些自己做的项目"),
        pc.divider(),
        component_grid(),
        text_align="left",
        margin_bottom="4em",
    )
