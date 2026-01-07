from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/')  

