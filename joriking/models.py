from django.db import models

# Create your models here.
class Joriking(models.Model):
    image = models.ImageField(upload_to='joriking/image/%Y/%m/%d')
    pred_path = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=255)
