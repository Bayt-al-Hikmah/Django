from django.db import models
from user.models import UserModel

class Todo(models.Model):
    user = models.ForeignKey(UserModel, related_name="tasks",on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
