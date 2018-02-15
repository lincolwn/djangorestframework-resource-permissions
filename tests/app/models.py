from django.db import models
from django.contrib.auth.models import User


class Office(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL)

class Issue(models.Model):
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL)

