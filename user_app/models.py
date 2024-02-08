from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    img = models.ImageField(upload_to="avatars_users", default="avatars_users/default.png",)
    login = models.CharField(max_length=50, unique=True, blank = True, null = True)
    channel_name = models.CharField(max_length=250, unique=True, blank = True, null = True)