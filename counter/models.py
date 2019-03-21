from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.FloatField(null=True, blank=True, default=0.0)
    key = models.CharField(max_length=10, unique=True, default="key")

    def __str__(self):
        return self.user.username
