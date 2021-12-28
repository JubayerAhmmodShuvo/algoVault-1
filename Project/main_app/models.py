from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, max_length=256)
    fullName = models.CharField(max_length=50, default="N/A")
    isVarified = models.BooleanField(default=False)
    auth_token = models.CharField(null=True, max_length=200)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username