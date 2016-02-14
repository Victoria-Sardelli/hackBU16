from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=32)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=32)


class Activity(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    approx_time = models.TimeField()
    due_date = models.DateField()
    priority = models.IntegerField(default=0)
