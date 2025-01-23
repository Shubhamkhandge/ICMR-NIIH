from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.http import QueryDict
from application.forms import CaptchaForm
from django.http import HttpRequest
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
from dateutil import relativedelta
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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
from .admin import *
#from datetime import datetime
# Create your views here.

# Home and basic pages
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

def awards_achievements(request):
    return render(request, 'awards-achievements.html')

def former_directors(request):
    return render(request, 'former-directors.html')

def contact_directory(request):
    return render(request, 'contact-directory.html')

# Department-related pages
def departments(request):
    d_name = dept_info.objects.values_list('department_id','lab_department_name','department_info')
    return render(request, 'departments.html',{'dept_info':d_name})
    
def departments_details(request):
    print(request.POST.get('dept_id'))
    if request.method == 'POST':
        department_info = dept_info.objects.filter(department_id=request.POST.get('dept_id')).values_list()
        project_list = projects.objects.filter(scientist_name = department_info[0][4]).values_list()
        res_staff_list = scientific_staff.objects.filter(lab_department_name = department_info[0][2]).values_list('scientist_name','designation')
        print(res_staff_list)
        return render(request, 'departments-details.html', {'dept_info':department_info, 'project':project_list, 'res_staff':res_staff_list})

# Staff-related pages
def scientist_staff(request):
    sci_staff = scientific_staff.objects.values_list('scientist_name','profilepic_name')
    return render(request, 'scientist-staff.html', {'scientist_staff':sci_staff})

def scientist_details(request):
    if request.method == 'POST':
        sci_info = scientific_staff.objects.filter(scientist_id = request.POST.get('sci_id')).values_list()
        return render(request, 'scientist-staff-details.html', {'scientist_info':sci_info})

def administration_staff(request):
    return render(request, 'administration-staff.html')

def administration_details(request):
    return render(request, 'administration-staff-details.html')

def technical_staff(request):
    return render(request, 'technical-staff.html')

def technical_details(request):
    return render(request, 'technical-staff-details.html')

def project_staff(request):
    return render(request, 'project-staff.html')

def project_details(request):
    return render(request, 'project-staff-details.html')

def students_list(request):
    return render(request, 'students-list.html')

def student_details(request):
    return render(request, 'student-staff-details.html')

def alumini_staff(request):
    return render(request, 'alumini-staff.html')

def alumini_details(request):
    return render(request, 'alumini-staff-details.html')

# Publications and News
def publications_list(request):
    return render(request, 'publications-list.html')

def niih_bulletin_list(request):
    return render(request, 'niih-bulletin-list.html')

def bgrc_news_letter(request):
    return render(request, 'bgrc-news-letter.html')

# Projects
def ongoing_projects_list(request):
    return render(request, 'ongoing-projects-list.html')

def completed_projects_list(request):
    return render(request, 'completed-projects-list.html')

# Media and Photo Details
def media_gallery(request):
    return render(request, 'media-gallery.html')

def photo_details(request):
    return render(request, 'photo-details.html')

# Reports and Cirulars, Tenders
def circulars_list(request):
    return render(request, 'circulars-list.html')

def advertise_list(request):
    return render(request, 'advertise-list.html')

def tenders_list(request):
    return render(request, 'tenders-list.html')

def reports_list(request):
    return render(request, 'reports-list.html')







    
        
