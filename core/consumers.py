import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CoreConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    async def connect(self):
        from django.contrib.auth.models import AnonymousUser
        self.scope["user"] = AnonymousUser()
        self.room_group_name = "public"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        from django.contrib.auth.models import AnonymousUser
        text_data_json = json.loads(text_data)
        if text_data_json.get("access_token") and not self.scope["user"].is_authenticated:
            self.scope["user"] = await verify_user(text_data_json.get("access_token"))
            if self.scope["user"].is_authenticated:
                user_id = str(self.scope["user"].id)
                await self.channel_layer.group_add(user_id, self.channel_name)
        elif text_data_json.get("logout"):
            if self.scope["user"].is_authenticated:
                user_id = str(self.scope["user"].id)
                await self.channel_layer.group_discard(user_id, self.channel_name)
            self.scope["user"] = AnonymousUser()

        else:
            pass

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def send_data(self, event):
        message = event['data']
        await self.send(text_data=json.dumps({
            'data': message
        }))


@database_sync_to_async
def verify_user(access_token: str):
    from django.contrib.auth.models import AnonymousUser
    try:
        c = JWTAuthentication()
        validated_token = c.get_validated_token(access_token)
        return c.get_user(validated_token)
    except Exception as e:
        print(e)
    return AnonymousUser()
