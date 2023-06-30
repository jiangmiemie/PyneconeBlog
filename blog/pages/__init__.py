from .index import index
from .project import project
from .gallery import gallery
from .month import month
from .code import code
from blog import tsclient
from blog.base_state import Route
from blog.templates.page import mdpage

routes = [r for r in locals().values() if isinstance(r, Route)]


for pagelist in tsclient.check_data():
    routes.append(
        Route(
            path=pagelist[1],
            title=pagelist[2],
            component=mdpage(pagelist[5], pagelist[1], pagelist[2], pagelist[4]),
        )
    )
