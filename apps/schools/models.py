from django.db import models

from apps.common.models import BaseModel

from autoslug import AutoSlugField


def slugify_name(self):
    return f"{self.name}"


class School(BaseModel):
    slug = AutoSlugField(unique=True, populate_from=slugify_name, always_update=True, null=True, blank=True)
    name= models.CharField(max_length=500)
    abv = models.CharField(null=True, blank=True, max_length=10)

    def __str_(self):
        return self.name