from django.db import models

# Create your models here.

class Wheel(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
