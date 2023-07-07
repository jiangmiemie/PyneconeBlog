from .pgsql import pgsql
from web.base_state import Route

pgsqlroutes = [r for r in locals().values() if isinstance(r, Route)]
