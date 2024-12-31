from django.contrib import admin
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.http import QueryDict
from application.forms import CaptchaForm
from django.http import HttpRequest
from django.contrib import messages
from .models import department_staff, departments, department
# Register your models here.
# Admin Dashboard Urls
def login_page(request):
    return render(request, 'admin_dashboard/login.html')

def dashboard_view(request):
    return render(request, 'admin_dashboard/dashboard.html')

def user_registration(request):
    return render(request, 'admin_dashboard/user_registration.html')

def user_registration(request):
    return render(request, 'admin_dashboard/user_registration.html')

def all_departments(request):
    return render(request, 'admin_dashboard/all_departments.html')

def add_department(request):
    return render(request, 'admin_dashboard/add_department.html')
            
def update_department(request):
    return render(request, 'admin_dashboard/update_department.html')
            
def all_scientists(request):
    return render(request, 'admin_dashboard/all_scientists.html')
                   
def add_scientist(request):
    return render(request, 'admin_dashboard/add_scientist.html')
            