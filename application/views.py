from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.http import QueryDict
from application.forms import CaptchaForm
from django.http import HttpRequest
from django.contrib import messages


from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
from dateutil import relativedelta
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import UserForm
from django.core.mail import send_mail, EmailMultiAlternatives
import random
from django.http import JsonResponse
import os
from django.core import serializers
from json import dumps
import json
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import csv
import xlwt
#from datetime import datetime
# Create your views here.

def home(request):
    return render(request, "index.html")

def vision_mission_mandate(request):
    return render(request, 'vision-mission-mandate.html')

def organogram(request):
    return render(request, 'organogram.html')
    
def niih_leadership(request):
    return render(request, 'niih-leadership.html')
    
def our_director(request):
    return render(request, 'our-director.html')

def departments(request):
    return render(request, 'departments.html')

def departments_details(request):
    return render(request, 'departments-details.html')

def scientists(request):
    return render(request, 'scientists.html')

def scientist_details(request):
    return render(request, 'scientist-details.html')

def awards_achievements(request):
    return render(request, 'awards-achievements.html')

def former_directors(request):
    return render(request, 'former-directors.html')

def contact_directory(request):
    return render(request, 'contact-directory.html')

