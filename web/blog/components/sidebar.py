import os
from blog.tsclient import Pagelist, check_data

FILE_DIR = os.path.join("assets", "pages")


def read_md():
    flat_items = []
    for i in check_data():
        p = Pagelist(
            path=i[1],
            title=i[2],
            category=i[3],
            time=i[4],
            contents=i[5],
        )
        flat_items.append(p)

    return flat_items


flat_items = read_md()


def get_prev_next(url):
    for i, item in enumerate(flat_items):
        if item.path == url:
            if i == 0 and len(flat_items) > 1:
                return None, flat_items[i + 1]
            elif i == len(flat_items) - 1:
                return flat_items[i - 1], None
            else:
                return flat_items[i - 1], flat_items[i + 1]
    return None, None
