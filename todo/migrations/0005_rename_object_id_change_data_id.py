# Generated by Django 4.2.1 on 2023-05-12 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_tag_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='change',
            old_name='object_id',
            new_name='data_id',
        ),
    ]
