from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .serializers import UserSerializer


def send2group(group_name: str, data) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'send_data',
        'data': data
    })


@receiver(post_save, sender=User, dispatch_uid="user_changed_signal")
def user_changed_signal(instance: User, **kwargs):
    if kwargs['created']:
        return

    data = UserSerializer(instance).data
    data['target'] = 'user'
    send2group(str(instance.id), data)
