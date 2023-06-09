from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Change, Tag, Task, Project, Shared
from .serializers import ChangeSerializer

User = get_user_model()


def send2group(group_name: str, data) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'send_data',
        'data': data
    })


@receiver(post_save)
def on_model_save(instance, **kwargs):
    table = None
    if isinstance(instance, Tag):
        table = Change.CHANGE_TAG
    elif isinstance(instance, Task):
        table = Change.CHANGE_TASK
    elif isinstance(instance, Project):
        table = Change.CHANGE_PROJECT
    elif isinstance(instance, User):
        table = Change.CHANGE_USER
    if not table:
        return

    action = Change.ACTION_UPDATE
    if kwargs['created']:
        action = Change.ACTION_CREATE
    Change.objects.filter(table=table, data_id=instance.id).delete()
    change = Change()
    if isinstance(instance, User):
        change.user = instance
    else:
        change.user = instance.user
    change.data_id = instance.id
    change.table = table
    change.action = action
    change.save()


@receiver(post_delete)
def on_model_delete(instance, **kwargs):
    table = None
    if isinstance(instance, Tag):
        table = Change.CHANGE_TAG
    elif isinstance(instance, User):
        table = Change.CHANGE_USER
    elif isinstance(instance, Task):
        table = Change.CHANGE_TASK
    elif isinstance(instance, Project):
        table = Change.CHANGE_PROJECT
    if not table:
        return
    # delete all changes for this instance
    Change.objects.filter(table=table, data_id=instance.id).delete()
    change = Change()
    if isinstance(instance, User):
        change.user = instance
    else:
        change.user = instance.user
    change.data_id = instance.id
    change.table = table
    change.action = Change.ACTION_DELETE
    change.save()


@receiver(post_save, sender=Change)
def on_change_notify_user(instance, **kwargs):
    if kwargs['created']:
        data = ChangeSerializer(instance).data
        data['target'] = 'change'
        send2group(str(instance.user.id), data)


@receiver(post_delete)
def clean_shared_on_delete_tag_project(instance, **kwargs):
    if isinstance(instance, Tag):
        Shared.objects.filter(table=Shared.SHARED_TAG, data_id=instance.id).delete()
    elif isinstance(instance, Project):
        Shared.objects.filter(table=Shared.SHARED_PROJECT, data_id=instance.id).delete()
