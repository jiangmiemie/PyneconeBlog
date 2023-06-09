import os
import pynecone as pc
from blog.tsclient import Pagelist, add_data

FILE_DIR = os.path.join("assets", "pages")


def read_md():
    flat_items = []
    for root, dirs, files in os.walk(FILE_DIR, topdown=False):
        for name in files:
            if ".png" in name:
                continue
            tag = root.replace(FILE_DIR, "").replace("\\", "")
            file_path = os.path.join(root, name)
            with open(file_path) as f:
                contents = f.read()
            filename = name.replace(".md", "")
            time = filename[:6]
            title = filename[6:]
            path = (
                file_path.replace(FILE_DIR, "")
                .replace("\\", "/")
                .replace(".md", "")
                .replace(time, "")
            )

            p = Pagelist(
                path=str(path.encode("utf-8"))
                .replace("b", "")
                .replace(r"\x", "")
                .replace("'", ""),
                tag=tag,
                title=title,
                time=int(time),
                contents=contents,
            )
            flat_items.append(p)
            add_data(p)
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
