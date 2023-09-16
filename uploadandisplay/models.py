from django.db import models
import os
# Create your models here.
class ImageModel(models.Model):
    Image = models.ImageField(upload_to='images')
    date = models.DateTimeField(auto_now_add=True)

# class File(models.Model):
#     file = models.FileField()
#     def filename(self):
#         return os.path.basename(self.file.name)