# Generated by Django 5.0.1 on 2024-04-01 09:17

import apps.crates.models
import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crate',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, blank=True, editable=False, null=True, populate_from=apps.crates.models.slugify_name, unique=True),
        ),
    ]
