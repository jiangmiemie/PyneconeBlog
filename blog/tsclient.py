import pynecone as pc
import psycopg2
from configparser import ConfigParser

from blog.constants import MAIN_URL


class Pagelist(pc.Model, table=True):
    path: str
    tag: str
    time: int
    title: str
    contents: str


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


def updata_data(sql):
    """
    插入2条数据， RUN 表示状态为正常，大小写敏感，如果插入数据有单引号如： jack's blog 需要改成 jack''s blog(变成2个单引号)
    INSERT INTO reflexblog ("indexs", "status", "name", "link") VALUES ('99998', 'RUN', '开往', 'https://github.com/travellings-link/travellings');
    INSERT INTO reflexblog ("indexs", "status", "name", "link") VALUES ('99999', 'RUN', '开往', 'https://github.com/travellings-link/travellings');

    修改示例 2，更新indexs值为99998的数据，设置它的状态值为'LOST'
    test3 = "UPDATE reflexblog SET status = 'LOST' WHERE indexs=99998"
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()


def check_data(sql="SELECT * FROM reflexblog WHERE indexs<1000"):
    """
    查询示例， 查询indexs为'99998'的数据
    test4 = "SELECT * FROM reflexblog WHERE indexs=99998"
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        db_version = cur.fetchall()
        conn.commit()
        cur.close()
        return db_version
    except (Exception, psycopg2.DatabaseError) as error:
        pass
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
        head = pagelist.title
        page = pagelist.contents
        if search_parameters in head:
            search = {
                "document": {
                    "heading": head,
                    "description": split_page(page, search_parameters, mode=1),
                    "href": pagelist.path,
                }
            }
            info.append(search)
        elif search_parameters in page:
            search = {
                "document": {
                    "heading": head,
                    "description": split_page(page, search_parameters, mode=2),
                    "href": pagelist.path,
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
