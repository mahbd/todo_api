from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/core/", consumers.CoreConsumer.as_asgi()),
]