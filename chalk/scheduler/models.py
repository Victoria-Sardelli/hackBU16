from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True)
    email = models.CharField()
    password = models.CharField()


class Activity(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    approx_time = models.TimeField()
    due_date = models.DateField()
    priority = models.IntegerField(default=0)
