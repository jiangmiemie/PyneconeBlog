import pynecone as pc
from blog.constants import MAIN_URL, TEST


class Pagelist(pc.Model, table=True):
    path: str
    tag: str
    time: int
    title: str
    contents: str


def add_data(p):
    if TEST:
        return []
    with pc.session() as session:
        if not check_data_by_path(p.path):
            session.add(p)
            session.commit()
        else:
            pass


def check_data():
    if TEST:
        return []
    with pc.session() as session:
        pagelists = session.query(Pagelist).filter(Pagelist.path != None)
    return pagelists


def check_data_by_tag(tag):
    if TEST:
        return []
    with pc.session() as session:
        pagelists = session.query(Pagelist).filter(Pagelist.tag == tag)
    return pagelists


def check_data_by_path(path):
    if TEST:
        return []
    p = []
    with pc.session() as session:
        pagelists = session.query(Pagelist).filter(Pagelist.path == path)
    for i in pagelists:
        p.append(i)
    return p


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
