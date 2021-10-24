from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.TextField(max_length=50, default='N/A')
    lastName = models.TextField(max_length=50, null=True, blank=True)
    isVarified = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username