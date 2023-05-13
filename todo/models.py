from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.title}'

    class Meta:
        ordering = ['title']
        unique_together = (('user', 'title'),)


class Change(models.Model):
    CHANGE_TASK = 'task'
    CHANGE_PROJECT = 'project'
    CHANGE_TAG = 'tag'
    CHANGE_USER = 'user'
    CHANGE_SHARED = 'shared'

    CHANGE_TYPE_CHOICES = [
        (CHANGE_TASK, 'Task'),
        (CHANGE_PROJECT, 'Project'),
        (CHANGE_TAG, 'Tag'),
        (CHANGE_USER, 'User'),
        (CHANGE_SHARED, 'Shared'),
    ]

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    ACTION_TYPE_CHOICES = [
        (ACTION_CREATE, 'Create'),
        (ACTION_UPDATE, 'Update'),
        (ACTION_DELETE, 'Delete'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.CharField(max_length=255, choices=CHANGE_TYPE_CHOICES)
    action = models.CharField(max_length=255, choices=ACTION_TYPE_CHOICES)
    data_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.title}'

    class Meta:
        ordering = ['-created_at']
