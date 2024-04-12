# Generated by Django 5.0.1 on 2024-04-12 04:05

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_sesson_key_guestuser_session_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(max_length=70, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('bd65a58d-7835-4079-8bfd-fbab159f2140'), primary_key=True, serialize=False, unique=True),
        ),
    ]
