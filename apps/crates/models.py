from django.db import models

from apps.common.models import BaseModel
from apps.schools.models import School
from apps.accounts.models import User

from autoslug import AutoSlugField

def slugify_name(self):
    return f"{self.name}"

class Crate(BaseModel):
    slug = AutoSlugField(unique=True, populate_from=slugify_name, always_update=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_crates')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_crates')

    def __str__(self):
        return self.name
