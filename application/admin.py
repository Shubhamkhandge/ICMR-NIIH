import datetime
from django.contrib import admin
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.http import QueryDict
from application.forms import CaptchaForm
from django.http import HttpRequest
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
# Admin Dashboard Urls
# Register your models here.
def login_page(request):
    return render(request, 'admin_dashboard/login.html')

#Dashboard View 
def dashboard_view(request):
    return render(request, 'admin_dashboard/dashboard.html')

# Registration page
def user_registration(request):
    return render(request, 'admin_dashboard/user_registration.html')

# About Pages
def vision_info(request):
    return render(request, 'admin_dashboard/vision_info.html')

# Department pages
def all_departments(request):
    deptinfo = dept_info.objects.values()
    return render(request, 'admin_dashboard/all_departments.html',{'all_dept':deptinfo})

def add_department_info(request):
    scientist_name = scientific_staff.objects.values_list('scientist_name')
    dropdept = support_department.objects.values_list('department_name')
    dropdesig = staff_designation.objects.filter(department = 'Scientist').values_list('designation')
    param={'dropdept':dropdept,'dropdesig':dropdesig,'scientist_name':scientist_name}
    if request.method == 'POST':
        department_info = dept_info(
            department_id = request.POST.get('department_id'),
            lab_department_name = request.POST.get('lab_department_name'),
            scientist_name = request.POST.get('scientist_name'),
            department_name = request.POST.get('department_name'),
            staff_designation = request.POST.get('staff_designation'),
            staff_email = request.POST.get('staff_email'),
            department_info = request.POST.get('department_info'),
            about_department1 = request.POST.get('about_department1'),
            about_department2 = request.POST.get('about_department2'),
            about_department3 = request.POST.get('about_department3'),
            about_research = request.POST.get('about_research')
        )
        department_info.save()
        messages.success(request, 'Department Information Added Successfully')
        return redirect('add_department_info')
    return render(request, 'admin_dashboard/add_department_info.html',param)

    # return render(request, 'admin_dashboard/add_department_info.html')
            
def update_department_info(request):
    return render(request, 'admin_dashboard/update_department_info.html')

def all_support_departments(request):
    support_deptinfo = support_department.objects.values()
    return render(request, 'admin_dashboard/all_support_departments.html', {'all_support_dept': support_deptinfo})

def add_support_department_info(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        hod_id = request.POST.get('hod_id')
        hod_name = request.POST.get('hod_name')
        deptSuppInfo = support_department(
            department_id=department_id,
            department_name=department_name,
            hod_id=hod_id,
            hod_name=hod_name
        )
        deptSuppInfo.save()
        return redirect('all_support_departments')
    return render(request, 'admin_dashboard/add_support_departments_info.html')

def update_support_department_info(request):
    if request.method == 'POST':
        if request.POST.get('update_data') == 'update_data':
            print(request.POST.get('department_name'))
            support_department.objects.filter(department_id=request.POST.get('department_id')).update(
                    department_name=request.POST.get('department_name'),
                    hod_id=request.POST.get('hod_id'),
                    hod_name=request.POST.get('hod_name')
                )
            support_deptinfo = support_department.objects.values()
            return render(request, 'admin_dashboard/all_support_departments.html', {'all_support_dept': support_deptinfo})

        update_support= support_department.objects.filter(department_id=request.POST.get('department_id')).values()
        param={'update_data':update_support}
        # print(update_support)
        return render(request, 'admin_dashboard/update_support_department_info.html',param)
        # support_department.objects.filter(id=request.post.get('id')).update()
    return render(request, 'admin_dashboard/update_support_department_info.html')

def delete_support_department(request):
    if request.method == 'POST':
        if request.POST.get('delete_data') == 'delete_data':
            support_department.objects.get(department_id=request.POST.get('department_id')).delete()
            support_deptinfo = support_department.objects.values()
            return render(request, 'admin_dashboard/all_support_departments.html', {'all_support_dept': support_deptinfo})

    return render(request, 'admin_dashboard/delete_support_department.html')

#  Designation pages
def all_designations(request):
    all_desig = staff_designation.objects.values()
    return render(request, 'admin_dashboard/all_designations.html', {'all_designation': all_desig})

def add_designation_info(request):
    department_name = support_department.objects.values_list('department_name')
    param={'department_name':department_name}
    print(department_name)
    if request.method == 'POST':
        desig_name = request.POST.get('designation_name')
        dept_name = request.POST.get('department_name')
        print(staff_designation.objects.filter(designation = desig_name, department = dept_name).values_list())
        if not staff_designation.objects.filter(designation = desig_name, department = dept_name).exists():
            desig = staff_designation(
                designation = desig_name,
                department = dept_name
            )
            desig.save()
        return redirect('all_designations')
    return render(request, 'admin_dashboard/add_designation_info.html', param)
        
            
def update_designation_info(request):
    return render(request, 'admin_dashboard/update_designation_info.html')
            
def delete_designation_info(request):
    if request.method == 'POST':
        if staff_designation.objects.filter(designation = request.POST.get('designation'), department = request.POST.get('department')).exists():
            if request.POST.get('delete_data') == 'delete_data':
                staff_designation.objects.filter(
                    designation=request.POST.get('designation'),
                    department=request.POST.get('department')
                ).delete()
                all_desig = staff_designation.objects.values()
                return render(request, 'admin_dashboard/all_designations.html', {'all_designation': all_desig})
    return render(request, 'admin_dashboard/delete_designation_info.html')

# Staff Pages
# Scientists Staff
def all_scientists_staff(request):
    all_scientist = scientific_staff.objects.values()
    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist})
                   
def add_scientist_info(request):
    dropdept = support_department.objects.values_list('department_name')
    dropdesig = staff_designation.objects.filter(department = 'Scientist').values_list('designation')
    param={'dropdept':dropdept,'dropdesig':dropdesig}
    if request.method == 'POST':
        if request.FILES.get('profilepic_name'):
            fs = FileSystemStorage(location="application/static/dist/images/staff/scientists")
            photo=request.FILES['profilepic_name']
            photo = fs.save(photo.name, photo)
            
            uploaded_photo = fs.url(photo).replace('/media/','').replace('%20',' ')
            print(dropdesig)
            print("----------------------------------------------")
            sci_info = scientific_staff(
                scientist_id = request.POST.get('scientist_id'),
                scientist_name = request.POST.get('scientist_name'),
                department_name = request.POST.get('department_name'),
                designation = request.POST.get('designation'),
                email_id = request.POST.get('email_id'),
                alt_email_id = request.POST.get('alt_email_id'),
                phone_no = request.POST.get('phone_no'),
                fax_no = request.POST.get('fax_no'),
                status = request.POST.get('status'),
                profilepic_name = uploaded_photo,
                research_interests = request.POST.get('research_interests'),
                academic_background = request.POST.get('academic_background'),
                professional_experience = request.POST.get('professional_experience'),
                data_created = datetime.datetime.now()
            )
            sci_info.save()
            return redirect('all_scientists_staff')
        else:
            sci_info = scientific_staff(
                scientist_id = request.POST.get('scientist_id'),
                scientist_name = request.POST.get('scientist_name'),
                department_name = request.POST.get('department_name'),
                designation = request.POST.get('designation'),
                email_id = request.POST.get('email_id'),
                alt_email_id = request.POST.get('alt_email_id'),
                phone_no = request.POST.get('phone_no'),
                fax_no = request.POST.get('fax_no'),
                status = request.POST.get('status'),
                research_interests = request.POST.get('research_interests'),
                academic_background = request.POST.get('academic_background'),
                professional_experience = request.POST.get('professional_experience'),
                data_created = datetime.datetime.now()
            )
            sci_info.save()
            return redirect('all_scientists_staff')
    return render(request, 'admin_dashboard/add_scientist_info.html', param)
                            
def update_scientist_info(request):
    if request.method == 'POST':
        #print(request.FILES['profilepic_name'],request.POST.get['profilepic_name'])
        if request.POST.get('update_data') == 'update_data':
            if request.FILES.get('profilepic_name'):
                fs = FileSystemStorage(location="application/static/dist/images/staff/scientists")
                photo = request.FILES['profilepic_name']
                photo = fs.save(photo.name, photo)
                uploaded_photo = fs.url(photo).replace('/media/', '').replace('%20', ' ')
                scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).update(
                    profilepic_name = uploaded_photo,
                    scientist_name = request.POST.get('scientist_name'),
                    department_name = request.POST.get('department_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    phone_no = request.POST.get('phone_no'),
                    fax_no = request.POST.get('fax_no'),
                    status = request.POST.get('status'),
                    research_interests = request.POST.get('research_interests'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                all_scientist = scientific_staff.objects.values()
                return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist})
            else:
                scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).update(
                    scientist_name = request.POST.get('scientist_name'),
                    department_name = request.POST.get('department_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    phone_no = request.POST.get('phone_no'),
                    fax_no = request.POST.get('fax_no'),
                    status = request.POST.get('status'),
                    research_interests = request.POST.get('research_interests'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                    )
                all_scientist = scientific_staff.objects.values()
                return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist})
        update_scientist = scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).values()
        dropdept = support_department.objects.values_list('department_name')
        dropdesig = staff_designation.objects.filter(department = 'Scientist').values_list('designation')
        param = {'update_data':update_scientist,'dropdesig':dropdesig, 'dropdept':dropdept}
        
        return render(request, 'admin_dashboard/update_scientist_info.html',param)
    return render(request, 'admin_dashboard/update_scientist_info.html')

def delete_scientist(request):
    if request.method == 'POST':
        if scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).exists():
            if request.POST.get('delete_data') == 'delete_data':
                scientific_staff.objects.filter(
                    scientist_id = request.POST.get('scientist_id')
                ).delete()
                all_scientist = scientific_staff.objects.values()
                return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist})
    return render(request, 'admin_dashboard/delete_scientist.html')

# Admin Staff
def all_admin_staff(request):
    return render(request, 'admin_dashboard/all_admin_staff.html')
                   
def add_admin_info(request):
    return render(request, 'admin_dashboard/add_admin_info.html')
                            
def update_admin_info(request):
    return render(request, 'admin_dashboard/update_admin_info.html')

# Technical Staff   

# Project Pages
def all_projects(request):
    dropdept = support_department.objects.values_list('department_name','hod_name')
    param={'dropdept':dropdept} 
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        project_status = request.POST.get('status')
        project_date = request.POST.get('project_date')
        project_data = project_new(
            project_title=project_title,
            hod_name=dropdept,
            department_name=dropdept,
            status=project_status,
            project_date=project_date
        )
        project_data.save()
        return redirect('all_projects')
    return render(request, 'admin_dashboard/all_projects.html', param)

def add_project_info(request):
    return render(request, 'admin_dashboard/add_project_info.html')

# Settings Page
def settings_page(request):
    return render(request, 'admin_dashboard/settings.html')