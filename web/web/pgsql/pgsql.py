import asyncio
import pynecone as pc
from web import constants
from web.page import webpage
from web.base_state import State
import psycopg2
from configparser import ConfigParser
from collections.abc import Iterable
from web.constants import MAIN_URL


class Pagelist:
    def __init__(self, path, category, time, title, contents) -> None:
        self.path = path
        self.category = category
        self.time = time
        self.title = title
        self.contents = contents


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


def init_db():
    try:
        updata_data("""DROP TABLE reflexblog""")
    except:
        pass

    updata_data(
        """CREATE TABLE "reflexblog" (
    "index"	INT,
    "path"	VARCHAR(512),
    "title"	VARCHAR(512),
    "category"	VARCHAR(512),
    "time"	VARCHAR(512),
    "contents"	text
);"""
    )

    for i in range(10):
        index = path = category = title = time = contents = i
        updata_data(
            """INSERT INTO reflexblog ("index","path", "category", "title","time", "contents") VALUES ('{}','{}','{}','{}','{}','{}');""".format(
                index,
                path,
                category,
                title,
                time,
                contents,
            )
        )


def updata_data(sql):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    finally:
        if conn is not None:
            conn.close()


def check_data(sql="SELECT * FROM reflexblog WHERE index<1000"):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        db = cur.fetchall()
        conn.commit()
        cur.close()

        if isinstance(db, Iterable):
            return db
        return []
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    finally:
        if conn is not None:
            conn.close()


def split_page(page: str, text: str, mode: int):
    lens = 50

    if len(page) <= lens:
        return page
    if len(text) >= lens:
        return text
    if mode == 1:
        return page[:lens]
    else:
        frot = page[: page.index(text)]
        back = page[page.index(text) + len(text) :]

        split_lens = lens - len(text)
        half_split_lens = int(split_lens / 2)

        if len(frot) > half_split_lens and len(back) > half_split_lens:
            frot = frot[0 - half_split_lens :]
            back = back[:half_split_lens]
        if len(frot) < half_split_lens and len(back) > half_split_lens:
            back = back[: split_lens - len(frot)]
        if len(frot) > half_split_lens and len(back) < half_split_lens:
            frot = frot[len(back) - split_lens :]
        return frot + text + back


def get_search(search_parameters):
    info = []

    pagelists = check_data()

    for pagelist in pagelists:
        head = pagelist[2]
        page = pagelist[5]
        if search_parameters in head:
            search = {
                "document": {
                    "heading": head,
                    "description": split_page(page, search_parameters, mode=1),
                    "href": pagelist[1],
                }
            }
            info.append(search)
        elif search_parameters in page:
            search = {
                "document": {
                    "heading": head,
                    "description": split_page(page, search_parameters, mode=2),
                    "href": pagelist[1],
                }
            }
            info.append(search)
    return info


def client(search_parameters):
    info = get_search(search_parameters)
    if info:
        return tuple(info)
    else:
        return (
            {
                "document": {
                    "heading": "没有找到你要的内容",
                    "description": "不妨回主页看看",
                    "href": MAIN_URL,
                }
            },
        )


class NavbarState(State):
    sidebar_open: bool = False

    search_modal: bool = False

    search_input: str = ""

    def change_search(self):
        self.search_modal = not (self.search_modal)

    def toggle_sidebar(self):
        """Toggle the sidebar open state."""
        self.sidebar_open = not self.sidebar_open

    @pc.var
    def search_results(self) -> list[dict[str, dict[str, str]]]:
        if self.search_input == "":
            return []
        return client(self.search_input)


def format_search_results(result):
    return pc.vstack(
        pc.link(
            pc.text(
                result["document"]["heading"],
                font_weight=600,
                color=constants.DOC_HEADER_COLOR,
            ),
            pc.divider(),
            pc.text(
                result["document"]["description"],
                font_weight=400,
                color=constants.DOC_REG_TEXT_COLOR,
            ),
            href=result["document"]["href"],
        ),
        on_click=NavbarState.change_search,
        border_radius="0.5em",
        width="100%",
        align_items="start",
        padding="0.5em",
        _hover={"background_color": "#e3e3e3c"},
    )


def get_search():
    return pc.box(
        pc.form(
            pc.input(
                placeholder="查找文章",
                on_change=NavbarState.set_search_input,
                _focus={
                    "border": f"2px solid {constants.ACCENT_COLOR}",
                },
                backdrop_filter="blur(10px)",
            ),
            on_submit=NavbarState.change_search,
        ),
    )


class IndexState(State):
    show_confetti: bool = False

    def start_confetti(self):
        """Start the confetti."""
        self.show_confetti = True
        return self.stop_confetti

    async def stop_confetti(self):
        """Stop the confetti."""
        await asyncio.sleep(5)
        self.show_confetti = False


@webpage()
def pgsql() -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.center(
                pc.vstack(
                    pc.button(
                        "重置测试数据",
                        width="50%",
                    ),
                    pc.container(
                        pc.form(
                            pc.input(
                                placeholder="智能查找",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                        pc.form(
                            pc.input(
                                placeholder="数据库语法：查",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                        pc.form(
                            pc.input(
                                placeholder="数据库语法：增删改",
                                on_change=NavbarState.set_search_input,
                                _focus={
                                    "border": f"2px solid {constants.ACCENT_COLOR}",
                                },
                                backdrop_filter="blur(10px)",
                            ),
                            on_submit=NavbarState.change_search,
                        ),
                    ),
                    justify="space-evenly",
                ),
                spacing="2em",
            ),
            justify="space-evenly",
        ),
        padding_y="5em",
        width="100%",
        background_image="/grid.png",
        background_repeat="no-repeat",
        background_position="top",
    )
