from django.db import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete = models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
  