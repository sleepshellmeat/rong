from django.db import models

# Create your models here.

class Grades(models.Model):
    gname = models.CharField(max_length=16)
    gdata = models.CharField(max_length=16)
    ggirlnum = models.IntegerField()
    gboynum = models.IntegerField()
    isDelete = models.BooleanField(default=False)


class Students(models.Model):
    sname = models.CharField(max_length=16)
    sgender = models.BooleanField(default=False)
    sage = models.IntegerField()
    scontend = models.CharField(max_length=100)
    isDelete = models.BooleanField(default=False)

    sgrade = models.ForeignKey("Grades")