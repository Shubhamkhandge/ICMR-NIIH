import datetime
from django.contrib import admin
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
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
    CaptchaForm1 = CaptchaForm(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if CaptchaForm1.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user'] = username
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_dashboard/login.html', {'CaptchaForm1': CaptchaForm1})

def logout_page(request):
    if 'user' in request.session:
        try:
            del request.session['user']
        except:
            pass
        logout(request)
    return redirect('login')
    # return render(request, 'admin_dashboard/logout.html')

#Dashboard View 
def dashboard_view(request):
    if 'user' in request.session:
        total_departments = dept_info.objects.count()
        total_categories = category.objects.count()
        total_projects = projects.objects.count()
        total_scientists = scientific_staff.objects.count()

        # Assuming 'project_status' field to differentiate between ongoing and completed projects
        ongoing_projects = projects.objects.filter(project_status='on going').count()
        completed_projects = projects.objects.filter(project_status='completed').count()

        context = {
            'username': request.session['user'],
            'total_departments': total_departments,
            'total_categories': total_categories,
            'total_projects': total_projects,
            'total_scientists': total_scientists,
            'ongoing_projects': ongoing_projects,
            'completed_projects': completed_projects,
        }
        return render(request, 'admin_dashboard/dashboard.html', context)
    return redirect('login')

# Registration page
def admin_user_registration(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/admin_user_registration.html')
    return redirect('login')
    

def add_admin_user(request):
    CaptchaForm1 = CaptchaForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password is not None:
            if password == cpassword:
                user = authenticate(username = username , password = password)
                if user is not None:
                    messages.warning(request, 'Username already exists.')
                else:
                    user = User.objects.create_user(username = username , password = password)
                    user.save()
                    messages.success(request, 'User created successfully')
                    return redirect('login')
    return render(request, 'admin_dashboard/add_admin_user.html', {'CaptchaForm1': CaptchaForm1})


# Settings Page
def settings_page(request):
    if 'user' in request.session:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    userChng = User.objects.get(username = request.session['user'])
                    userChng.set_password(password)
                    userChng.save()
                    messages.success(request, 'Password changed successfully')
                messages.warning(request, 'InValid Username!!')
            messages.warning(request, "Password Not Match!!")
        userInfo = User.objects.filter(username = request.session['user']).values()
        return render(request, 'admin_dashboard/settings.html', {'userInfo': userInfo, 'username': request.session['user']})
    return redirect('settings')

# About Pages
def vision_info(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/vision_info.html')
    return redirect('login')

# Department pages
def all_departments(request):
    if 'user' in request.session:
        deptinfo = dept_info.objects.values()
        return render(request, 'admin_dashboard/all_departments.html',{'all_dept':deptinfo, 'username': request.session['user']})
    return redirect('login')

def add_department_info(request):
    if 'user' in request.session:
        scientist_name = scientific_staff.objects.values_list('scientist_name')
        category_name = category.objects.filter(category_name = 'Scientist').values_list('category_name')
        dropdesig = staff_designation.objects.filter(category_name = 'Scientist').values_list('designation')
        param={'category_name':category_name,'dropdesig':dropdesig,'scientist_name':scientist_name,'username': request.session['user']}
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
            return redirect('all_departments')
        return render(request, 'admin_dashboard/add_department_info.html',param)
    return redirect('login')
            
def update_department_info(request):
    if 'user' in request.session:
        print(request.POST.get('scientist_name'))
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                dept_info.objects.filter(department_id = request.POST.get('department_id')).update(
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
                deptInfo = dept_info.objects.values()
                messages.success(request, 'Department Information Updated Successfully')
                return render(request, 'admin_dashboard/all_departments.html',{'all_dept':deptInfo})
            
            update_dept = dept_info.objects.filter(department_id=request.POST.get('department_id')).values()
            sci_name = scientific_staff.objects.values_list('scientist_name')
            category_name = category.objects.filter(category_name = 'Scientist').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Scientist').values_list('designation')
            param={'update_data':update_dept,'dropdesig':dropdesig,'category_name':category_name,'scientist_name':sci_name, 'username': request.session['user']}

        return render(request, 'admin_dashboard/update_department_info.html',param)
    return redirect('login')

def delete_department(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # if dept_info.objects.filter(department_id = request.POST.get('department_id')).exists():
            if request.POST.get('delete_data') == 'delete_data':
                dept_info.objects.filter(department_id = request.POST.get('department_id')).delete()
                deptinfo = dept_info.objects.values()
                return render(request, 'admin_dashboard/all_departments.html',{'all_dept':deptinfo, 'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_department.html', {'username': request.session['user']})

def all_categories(request):
    if 'user' in request.session:
        category_info = category.objects.values()
        return render(request, 'admin_dashboard/all_categories.html', {'all_cat_info': category_info, 'username': request.session['user']})
    return redirect('login')

def add_category_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            print(category.objects.filter(category_id = request.POST.get('category_id'), category_name = request.POST.get('category_name')).exists())
            if category.objects.filter(category_id = request.POST.get('category_id'), category_name = request.POST.get('category_name')).exists() == False:
                category_id = request.POST.get('category_id')
                category_name = request.POST.get('category_name')
                hod_id = request.POST.get('hod_id')
                hod_name = request.POST.get('hod_name')
                deptSuppInfo = category(
                    category_id=category_id,
                    category_name=category_name,
                    hod_id=hod_id,
                    hod_name=hod_name
                )
                deptSuppInfo.save()
                return redirect('all_categories')
        messages.warning(request, 'Duplliate entries are not allowed!!')
        print('messages')
        return render(request, 'admin_dashboard/add_category_info.html', {'username': request.session['user']})
    return redirect('login')

def update_category_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print(request.POST.get('category_name'))
                category.objects.filter(category_id=request.POST.get('category_id')).update(
                        category_name=request.POST.get('category_name'),
                        hod_id=request.POST.get('hod_id'),
                        hod_name=request.POST.get('hod_name')
                    )
                category_info = category.objects.values()
                return render(request, 'admin_dashboard/all_categories.html', {'all_cat_info': category_info})

            update_category= category.objects.filter(category_id=request.POST.get('category_id')).values()
            param={'update_data':update_category,'username': request.session['user']}
            print(update_category)
            return render(request, 'admin_dashboard/update_category_info.html', param)
            # category.objects.filter(id=request.post.get('id')).update()
        return render(request, 'admin_dashboard/update_category_info.html')
    return redirect('login')

def delete_category(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('delete_data') == 'delete_data':
                category.objects.filter(category_id=request.POST.get('category_id')).delete()
                category_info = category.objects.values()
                return render(request, 'admin_dashboard/all_categories.html', {'all_cat_info': category_info, 'username': request.session['user']})

        return render(request, 'admin_dashboard/delete_category.html', {'username': request.session['user']})

#  Designation pages
def all_designations(request):
    if 'user' in request.session:
        all_desig = staff_designation.objects.values()
        return render(request, 'admin_dashboard/all_designations.html', {'all_designation': all_desig, 'username': request.session['user']})
    return redirect('login')

def add_designation_info(request):
    if 'user' in request.session:
        category_name = category.objects.values_list('category_name')
        param={'category_name':category_name,'username': request.session['user']}
        print(category_name)
        if request.method == 'POST':
            desig_name = request.POST.get('designation')
            cat_name = request.POST.get('category_name')
            # print(staff_designation.objects.filter(designation = desig_name, department = cat_name).values_list())
            if not staff_designation.objects.filter(designation = desig_name, category_name = cat_name).exists():
                desig = staff_designation(
                    designation = desig_name,
                    category_name = cat_name
                )
                desig.save()
            return redirect('all_designations')
        return render(request, 'admin_dashboard/add_designation_info.html', param)
    return redirect('login')
        
            
def update_designation_info(request):
    if 'user' in request.session:
        designation_name = staff_designation.objects.filter(designation = request.POST.get('designation')).values()
        category_name = category.objects.values_list('category_name')
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print(request.POST.get('designation'),request.POST.get('category_name'))
                staff_designation.objects.filter(id=request.POST.get('id')).update(
                    designation = request.POST.get('designation'),
                    category_name = request.POST.get('category_name'),
                )
                return redirect('all_designations')
        return render(request, 'admin_dashboard/update_designation_info.html', {'update_data': designation_name, 'category_name': category_name,'username': request.session['user']})
    return redirect('login')
            
def delete_designation_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if staff_designation.objects.filter(designation = request.POST.get('designation'), category_name = request.POST.get('category_name')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    staff_designation.objects.filter(
                        designation=request.POST.get('designation'),
                        category_name=request.POST.get('category_name')
                    ).delete()
                    all_desig = staff_designation.objects.values()
                    return render(request, 'admin_dashboard/all_designations.html', {'all_designation': all_desig, 'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_designation_info.html', {'username': request.session['user']})

# Staff Pages
# Scientists Staff
def all_scientists_staff(request):
    if 'user' in request.session:
        all_scientist = scientific_staff.objects.values()
        return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist, 'username': request.session['user']})
    return redirect('login')
                   
def add_scientist_info(request):
    if 'user' in request.session:
        lab_department_name = dept_info.objects.values_list('lab_department_name')
        category_name = category.objects.filter(category_name = 'Scientist').values_list('category_name')
        dropdesig = staff_designation.objects.filter(category_name = 'Scientist').values_list('designation')
        param={'category_name':category_name,'dropdesig':dropdesig, 'lab_department_name': lab_department_name,'username': request.session['user']}
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
                    lab_department_name = request.POST.get('lab_department_name'),
                    category_name = request.POST.get('category_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    author_name = request.POST.get('author_name'),
                    phone_no = request.POST.get('phone_no'),
                    alt_phone_no = request.POST.get('alt_phone_no'),
                    aadhar_no = request.POST.get('aadhar_no'),
                    # guide_name = request.POST.get('guide_name'),
                    fax_no = request.POST.get('fax_no'),
                    profile_status = request.POST.get('profile_status'),
                    level_no = request.POST.get('level_no'),
                    join_year = request.POST.get('join_year'),
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
                    lab_department_name = request.POST.get('lab_department_name'),
                    category_name = request.POST.get('category_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    phone_no = request.POST.get('phone_no'),
                    alt_phone_no = request.POST.get('alt_phone_no'),
                    fax_no = request.POST.get('fax_no'),
                    author_name = request.POST.get('author_name'),
                    level_no = request.POST.get('level_no'),
                    aadhar_no = request.POST.get('aadhar_no'),
                    # guide_name = request.POST.get('guide_name'),
                    join_year = request.POST.get('join_year'),
                    profile_status = request.POST.get('profile_status'),
                    research_interests = request.POST.get('research_interests'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                sci_info.save()
                return redirect('all_scientists_staff')
        return render(request, 'admin_dashboard/add_scientist_info.html', param)
    return redirect('login')
                            
def update_scientist_info(request):
    if 'user' in request.session:
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
                        lab_department_name = request.POST.get('lab_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        author_name = request.POST.get('author_name'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        # guide_name = request.POST.get('guide_name'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        research_interests = request.POST.get('research_interests'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_scientist = scientific_staff.objects.values()
                    
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist,'level':level})
                else:
                    scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).update(
                        scientist_name = request.POST.get('scientist_name'),
                        lab_department_name = request.POST.get('lab_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        author_name = request.POST.get('author_name'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        # guide_name = request.POST.get('guide_name'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        research_interests = request.POST.get('research_interests'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_scientist = scientific_staff.objects.values()
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist})
            update_scientist = scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).values()
            lab_department_name = dept_info.objects.values_list('lab_department_name')
            category_name = category.objects.filter(category_name = 'Scientist').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Scientist').values_list('designation')
            level=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
            param = {'update_data':update_scientist,'dropdesig':dropdesig, 'lab_department_name':lab_department_name, 'category_name':category_name,'level':level,'username': request.session['user']}
            
            return render(request, 'admin_dashboard/update_scientist_info.html',param)
        return render(request, 'admin_dashboard/update_scientist_info.html')
    return redirect('login')

def delete_scientist(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).delete()
                    all_scientist = scientific_staff.objects.values()
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist,'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_scientist.html', {'username': request.session['user']})

# Admin Staff
def all_admin_staff(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/all_admin_staff.html', {'username': request.session['user']})
    return redirect('login')

def add_admin_info(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/add_admin_info.html', {'username': request.session['user']})
    return redirect('login')

def update_admin_info(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/update_admin_info.html', {'username': request.session['user']})
    return redirect('login')

# Technical Staff   

# Project Pages
def all_projects(request):
    if 'user' in request.session:
        all_project = projects.objects.values()
        ongoing_project = projects.objects.filter(project_status = 'On going').values()
        completed_project = projects.objects.filter(project_status = 'Completed').values()
        return render(request, 'admin_dashboard/all_projects.html', {'all_project': all_project, 'ongoing_project': ongoing_project , 'completed_project': completed_project, 'username': request.session['user']})
    return redirect('login')

def add_project_info(request):
    if 'user' in request.session:
        scientist_name = scientific_staff.objects.values_list('scientist_name')
        cat_name = category.objects.values_list('category_name')
        param={'category_name':cat_name, 'scientist_name':scientist_name, 'username': request.session['user']}
        if request.method == 'POST':
            project_data = projects(
                project_id = request.POST.get('project_id'),
                project_title = request.POST.get('project_title'),
                scientist_name = request.POST.get('scientist_name'),
                cat_name = request.POST.get('category_name'),
                project_status = request.POST.get('project_status'),
                project_date = datetime.datetime.now()
            )
            project_data.save()
            return redirect('all_projects') 
        return render(request, 'admin_dashboard/add_project_info.html', param)
    return redirect('login')

def update_project_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                projects.objects.filter(project_id = request.POST.get('project_id')).update(
                    project_title = request.POST.get('project_title'),
                    scientist_name = request.POST.get('scientist_name'),
                    category_name = request.POST.get('category_name'),
                    project_status = request.POST.get('project_status')
                )
                return redirect('all_projects')
            
            update_proj= projects.objects.filter(project_id=request.POST.get('project_id')).values()
            sci_name = scientific_staff.objects.values_list('scientist_name')
            category_name = category.objects.values_list('category_name')
            param={'update_data':update_proj,'category_name':category_name, 'scientist_name':sci_name, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_project_info.html',param)
    return redirect('login')

def delete_project(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # project_id = request.POST.get('project_id')
            projects.objects.filter(project_id = request.POST.get('project_id')).delete()
            return redirect('all_projects')
        return render(request, 'admin_dashboard/delete_project.html', {'username': request.session['user']})

