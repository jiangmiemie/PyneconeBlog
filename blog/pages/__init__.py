from .index import index
from .project import project
from .gallery import gallery
from .month import month
from .read import read
from .code import code
from blog import tsclient
from blog.route import Route
from blog.templates.page import mdpage

routes = [r for r in locals().values() if isinstance(r, Route)]

for pagelist in tsclient.check_data():
    routes.append(
        Route(
            path=pagelist.path,
            title=pagelist.title,
            component=mdpage(
                pagelist.contents, pagelist.path, pagelist.title, pagelist.time
            ),
        )
    )
