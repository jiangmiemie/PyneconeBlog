from .index import project
from web.base_state import Route

routes = [r for r in locals().values() if isinstance(r, Route)]
