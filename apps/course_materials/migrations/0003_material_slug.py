# Generated by Django 5.0.1 on 2024-04-01 09:17

import apps.course_materials.models
import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_materials', '0002_alter_material_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, blank=True, editable=False, null=True, populate_from=apps.course_materials.models.slugify_name, unique=True),
        ),
    ]