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

def awards_achievements(request):
    return render(request, 'awards-achievements.html')

def former_directors(request):
    return render(request, 'former-directors.html')

def contact_directory(request):
    return render(request, 'contact-directory.html')

def scientist_staff(request):
    return render(request, 'scientist-staff.html')

def scientist_details(request):
    return render(request, 'scientist-details.html')

def administration_staff(request):
    return render(request, 'administration-staff.html')

def administration_details(request):
    return render(request, 'administration-details.html')

def technical_staff(request):
    return render(request, 'technical-staff.html')

def technical_details(request):
    return render(request, 'technical-details.html')

def project_staff(request):
    return render(request, 'project-staff.html')

def project_details(request):
    return render(request, 'project-details.html')

def students_list(request):
    return render(request, 'students-list.html')

def student_details(request):
    return render(request, 'student-details.html')

def alumini_staff(request):
    return render(request, 'alumini-staff.html')

def alumini_details(request):
    return render(request, 'alumini-details.html')

def publications_list(request):
    return render(request, 'publications.html')

def niih_bulletin(request):
    return render(request, 'niih_bulletin.html')

def bgrc_news_letter(request):
    return render(request, 'bgrc-news-letter.html')

def projects_list(request):
    return render(request, 'projects-list.html')

def ongoing_projects(request):
    return render(request, 'ongoing-projects.html')

def completed_projects(request):
    return render(request, 'completed-projects.html')

def media_gallery(request):
    return render(request, 'media-gallery.html')

def circulars_list(request):
    return render(request, 'circulars-list.html')

def tenders_list(request):
    return render(request, 'tenders-list.html')

def reports_list(request):
    return render(request, 'reports-list.html')

