from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserApiData(models.Model):
    name = models.CharField(max_length=10)
    api_key = models.CharField(max_length=32)
    secret_key = models.CharField(max_length=32)