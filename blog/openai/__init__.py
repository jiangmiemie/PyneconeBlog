from .chatgpt import chatgpt
from .dalle import dalle
from .login import login
from blog.route import Route

openairoutes = [r for r in locals().values() if isinstance(r, Route)]
