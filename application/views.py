from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
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
from django.db.models import *
import csv
import xlwt
from .admin import *
from datetime import datetime
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
    sci_staff = scientific_staff.objects.values_list('scientist_name','profilepic_name', 'scientist_id','profile_status','author_name','designation','level_no','join_date','current_post_date','div_name')
    data_list = list(sci_staff) 
    
    # Sort in descending order (latest to oldest)
    data_list.sort(key=lambda x: x[8], reverse=False)
    data_list.sort(key=lambda x: x[6], reverse=True)
    # Print the sorted list
    
       #item[8] = datetime.strptime(item[8], "%Y-%m-%d")
    #sci_info1=sorted(sci_staff, key=lambda x: x["date"], reverse=True)
    #for item in sci_info1:
      #  print(f"Name: {item['8']}, Date: {item['8'].strftime('%Y-%m-%d')}")
    #sci_info = sorted(sci_staff, key=lambda x: (x[6], datetime.strptime(x[7])))
    
    # paginator = Paginator(sci_staff, 15)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'scientist-staff.html', {'scientist_staff':data_list})

def scientist_details_id(request, sci_id):#, auth_id):
    sci_info = scientific_staff.objects.filter(scientist_id = sci_id).values()
    project = projects.objects.filter(scientist_name = sci_info[0]['scientist_name']).values()
    awards = award_list.objects.filter(scientist_name = sci_info[0]['scientist_name']).values()
    findPub = sci_info[0]['author_name']
    # publications = publications_list.objects.values_list('publication_author_name')
    # print(publications[0][0].split(', '))
    publications = publications_list.objects.values_list('publication_author_name','publication_title','publication_journal_name','publication_status')
    pubauth = []
    for i in range(len(publications)):
        authpublst = publications[i][0].split(', ')
        for j in range(len(authpublst)):
            if authpublst[j] == findPub:
                pubauth.append(publications[i])
            
    #print(publications)
    
    str_academic_info = str(sci_info[0]['academic_background'])
    str_info = str(sci_info[0]['research_interests'])
    
    sci_info_academic = '<br> - '.join(str_academic_info.split('-')).strip()
    sci_info_sepc = '<br> - '.join(str_info.split('-')).strip()
    print(sci_info[0]['lab_department_name'])
    sci_staff=scientific_staff.objects.filter(lab_department_name=sci_info[0]['lab_department_name']).values_list()
    technical_staffs=technical_staff.objects.filter(support_department_name=sci_info[0]['lab_department_name']).values_list()
    return render(request, 'scientist-staff-details.html', {'scientist_info': sci_info[0], 'sci_spec': sci_info_sepc, 'project_info': project, 'award_info': awards , 'publication_info': pubauth , 'str_academic_info': sci_info_academic, 'technical_staff':technical_staffs, 'sci_staff':sci_staff})

def scientist_details(request):
    if request.method == 'POST':
        return redirect('scientist_details_id', sci_id=request.POST.get('sci_id'))#, auth_id=request.POST.get('auth_id'))
        #return render(request, 'scientist-staff-details.html')

def admin_staff(request):
    admin_staff = administration_staff.objects.values_list('admin_name','profilepic_name', 'admin_id','profile_status','designation','level_no','display_order','join_date','current_post_date','div_name').order_by('-display_order')
    # paginator = Paginator(admin_staff, 12)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'administration-staff.html', {'admin_staff_info':admin_staff})

def administration_details(request):
    if request.method == 'POST': 
        admin_info = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values()
        str_info=str(admin_info[0]['specialization'])
        admin_info_sepc = '<br> - '.join(str_info.split('-')).strip()
        return render(request, 'administration-staff-details.html', {'admin_info': admin_info[0], 'admin_spec': admin_info_sepc})
    return render(request, 'administration-staff-details.html')

def technical_staffs(request):
    tech_staff = technical_staff.objects.values_list('technical_name','profilepic_name', 'technical_id','profile_status','designation','level_no','current_post_date')
    # data_list = list(tech_staff) 

    # data_list.sort(key=lambda x: x[4])
    # data_list.sort(key=lambda x: x[5])
    '''paginator = Paginator(data_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)'''

    return render(request, 'technical-staff.html', {'technical_staff':tech_staff})

def technical_details(request):
    if request.method == 'POST': 
        tech_info = technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).values()
        # project = projects.objects.filter(technical_name = tech_info[0]['technical_name']).values()
        
        str_academic_info = str(tech_info[0]['academic_background'])
        str_info = str(tech_info[0]['specialization'])
        
        tech_info_academic = '<br> - '.join(str_academic_info.split('-')).strip()
        tech_info_sepc = '<br> - '.join(str_info.split('-')).strip()

        return render(request, 'technical-staff-details.html', {'technical_info': tech_info[0], 'tech_spec': tech_info_sepc, 'str_academic_info': tech_info_academic})
    return render(request, 'technical-staff-details.html')

def project_staff_info(request):
    proj_staff = project_staff.objects.values_list('project_staff_name', 'project_staff_designation', 'project_staff_department', 'profile_status')
    paginator = Paginator(proj_staff, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'project-staff.html', {'all_project_staff': proj_staff})

def project_details(request):
    return render(request, 'project-staff-details.html')

def students_list(request):
    all_students = student_staff.objects.values_list('student_staff_name', 'student_guide_name', 'student_staff_department', 'student_join_year','profile_status')
    # paginator = Paginator(all_students, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'students-list.html', {'all_student': all_students})

def student_details(request):
    return render(request, 'student-staff-details.html')

def alumini_list(request):
    all_aluminis = alumini_staff.objects.values_list('id','alumini_staff_name', 'alumini_staff_designation', 'alumini_leave_year','profile_status')
    paginator = Paginator(all_aluminis, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'alumini-staff.html', {'all_alumini': all_aluminis})


def alumini_details(request):
    return render(request, 'alumini-staff-details.html')

# Publications and News
def publications(request):
    all_publications = publications_list.objects.values_list()
    paginator = Paginator(all_publications, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'publications-list.html', {'publications':page_obj})

def niih_bulletin_list(request):
    all_niih_bulletins = bulletin_list.objects.values_list()
    paginator = Paginator(all_niih_bulletins, 45)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'niih-bulletin-list.html', {'all_bulletins':page_obj})

def bgrc_news_letter(request):
    all_newsletters = newsletter_list.objects.values_list()
    paginator = Paginator(all_newsletters, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bgrc-news-letter.html', {'all_news':all_newsletters})

# Projects
def ongoing_projects_list(request):
    all_project = projects.objects.values()
    ongoing_project = projects.objects.filter(project_status = 'On going').values()
    paginator = Paginator(ongoing_project, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ongoing-projects-list.html', {'projects':all_project, 'ongoing_project':page_obj})

def completed_projects_list(request):
    all_project = projects.objects.values()
    completed_project = projects.objects.filter(project_status = 'Completed').values()
    paginator = Paginator(completed_project, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'completed-projects-list.html', {'projects':all_project, 'completed_project':page_obj})

# Media and Photo Details
def media_gallery(request):
    all_media = media.objects.values_list()
    return render(request, 'media-gallery.html', {'media':all_media})

def photo_details(request):
    return render(request, 'photo-details.html')

# Reports and Cirulars, Tenders
def circulars_list(request):
    # Get filter values from the GET request
    name_filter = request.GET.get('nameFilter', '')
    from_year = request.GET.get('fromYear', '')

    # Base query to get all circulars
    # all_circular = CircularList.objects.all()

    # Apply filters if provided
    if name_filter:
        all_circular = all_circular.filter(circular_title__icontains=name_filter)
    if from_year:
        all_circular = all_circular.filter(circular_date__year=from_year)

    all_circular = circular_list.objects.values_list('circular_title', 'circular_date','circular_file_name', 'circular_status')
    paginator = Paginator(all_circular, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'circulars-list.html', {'all_circulars': page_obj})

def advertises(request):
    all_advertise = advertise_list.objects.values_list('advertise_title', 'advertise_date','advertise_file_name', 'advertise_status')
    paginator = Paginator(all_advertise, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'advertise-list.html', {'all_advertises':page_obj})

def tenders_list(request):
    all_tender = tender_list.objects.values_list('tender_title', 'tender_date','tender_file_name', 'tender_status')
    print(all_tender)
    paginator = Paginator(all_tender, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tenders-list.html', {'all_tenders':page_obj})

def reports_list(request):
    return render(request, 'reports-list.html')







    
        
