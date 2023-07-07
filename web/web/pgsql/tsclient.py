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
