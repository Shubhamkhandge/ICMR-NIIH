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
    
    
class scientific_staff(models.Model):
    name = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    image_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    fax = models.CharField(max_length=200, null=True)
    academic_background = models.TextField()
    professional_experience = models.TextField()
    research_interests = models.TextField()
    awards_achievements = models.TextField()
    publications = models.TextField()
    projects = models.TextField()
    research_staff = models.CharField(max_length=255, null=True)
    display_order = models.CharField(max_length=255, null=True)
    active = models.CharField(max_length=200, null=True)
    created = models.CharField(max_length=200, null=True)

class department(models.Model):
    sr_id = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    hod_id = models.CharField(max_length=255, null=True)
    hod_name = models.CharField(max_length=255, null=True)
    
class departments(models.Model):
    d_id = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    hod = models.CharField(max_length=200, null=True)
    about = models.TextField()
    display_order = models.CharField(max_length=255, null=True)
    created = models.CharField(max_length=255, null=True)



