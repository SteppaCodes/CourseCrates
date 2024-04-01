from django.db import models

from apps.accounts.models import User, LEVEL_CHOICES
from apps.common.models import BaseModel
from apps.crates.models import Crate
from apps.schools.models import School
from .customs import CustomGoogleDriveStorage

from autoslug import AutoSlugField

gd_storage = CustomGoogleDriveStorage()

class Course(BaseModel):
    code = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_courses')
    
    def __str__(self):
        return self.code

FILE_CATEGORY_CHOICES = (
    ('Note', 'Note'),('TextBook', 'TextBook'),('PQ & A', 'PQ & A')
)


def slugify_name(self):
    return f"{self.name}"

class Material(BaseModel):
    slug = AutoSlugField(unique=True, populate_from=slugify_name, always_update=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    file = models.FileField(upload_to='materials/', storage=gd_storage)
    category= models.CharField(max_length=200, choices=FILE_CATEGORY_CHOICES)
    crate = models.ForeignKey(Crate, on_delete=models.SET_NULL,null=True, blank=True, related_name='crate_materials')
    size = models.DecimalField(default=10, max_digits=6, decimal_places=2)                        
    owner = models.ForeignKey(User, related_name="owner_material", on_delete = models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_materials')
    level = models.CharField(max_length=200, choices=LEVEL_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
 

