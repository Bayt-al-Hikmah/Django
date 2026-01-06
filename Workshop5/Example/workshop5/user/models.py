from django.db import models
from django.contrib.auth.models import User

class UserModel(User):
    avatar = models.ImageField(upload_to='uploads/')  

# Create your models here.
