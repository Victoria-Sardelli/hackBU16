from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    approx_time = models.IntegerField(null=True)
    due_date = models.DateField()
    priority = models.IntegerField(default=0)


class Frees(models.Model):
    startTime = models.DateTimeField()
    finishTime = models.DateTimeField()
