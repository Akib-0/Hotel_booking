from django.db import models

# Create your models here.

class Area(models.Model):
    area_name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length= 100, unique = True)
    area_image = models.ImageField(upload_to = 'photos/categories', blank = True)
    
    def __str__(self):
        return self.area_name
