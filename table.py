import os
import pynecone as pc
from blog.tsclient import Pagelist, updata_data, init_db

FILE_DIR = os.path.join("assets", "pages")


def read_md():
    flat_items = []
    index = 0
    init_db()
    for root, dirs, files in os.walk(FILE_DIR, topdown=False):
        for name in files:
            if ".png" in name:
                continue
            tag = root.replace(FILE_DIR, "").replace("\\", "").replace("/", "")
            file_path = os.path.join(root, name)
            with open(file_path) as f:
                contents = f.read().replace("'", "''")
            filename = name.replace(".md", "")
            time = int(filename[:6])
            title = filename[6:]
            path = (
                str(
                    (
                        file_path.replace(FILE_DIR, "")
                        .replace("\\", "/")
                        .replace(".md", "")
                        .replace(str(time), "")
                    ).encode("utf-8")
                )
                .replace("b", "")
                .replace(r"\x", "")
                .replace("'", "")
            )

            updata_data(
                """INSERT INTO reflexblog ("index","path", "tag", "title","time", "contents") VALUES ('{}','{}','{}','{}','{}','{}');""".format(
                    index,
                    path,
                    tag,
                    title,
                    time,
                    contents,
                )
            )
            index += 1
    return flat_items


read_md()
