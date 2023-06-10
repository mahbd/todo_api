# Generated by Django 4.2.1 on 2023-05-12 12:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0003_change_object_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('user', 'title')},
        ),
    ]
