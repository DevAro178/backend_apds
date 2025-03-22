from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)  # Store Google API token
    profile_picture = models.URLField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    password=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.username
