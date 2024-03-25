from django.db import models

from apps.common.models import BaseModel


class School(BaseModel):
    name= models.CharField(max_length=500)
    abv = models.CharField(null=True, blank=True, max_length=10)

    def __str_(self):
        return self.name