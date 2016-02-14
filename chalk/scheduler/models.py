from django.db import models


# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    approx_time = models.TimeField()
    due_date = models.DateField()
    priority = models.IntegerField()
