import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo_api.settings")

import core.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(core.routing.websocket_urlpatterns),
        "http": django_asgi_app,
    }
)
