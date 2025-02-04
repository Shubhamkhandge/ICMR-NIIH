import datetime
import os
from django.conf import settings
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
        total_support_departments = support_department.objects.count()
        total_categories = category.objects.count()
        total_designations = staff_designation.objects.count()
        total_projects = projects.objects.count()
        total_scientists = scientific_staff.objects.count()
        total_admins = administration_staff.objects.count()
        total_technical = technical_staff.objects.count()
        total_publications = publications_list.objects.count()
        total_niih_bulletins = bulletin_list.objects.count()
        total_bgrc_newsletters = technical_staff.objects.count()
        total_awards = award_list.objects.count()

        # Assuming 'project_status' field to differentiate between ongoing and completed projects
        ongoing_projects = projects.objects.filter(project_status='on going').count()
        completed_projects = projects.objects.filter(project_status='completed').count()

        context = {
            'username': request.session['user'],
            'total_departments': total_departments,
            'total_support_departments': total_support_departments,
            'total_categories': total_categories,
            'total_designations': total_designations,
            'total_projects': total_projects,
            'total_scientists': total_scientists,
            'total_admins': total_admins,
            'total_technical': total_technical,
            'ongoing_projects': ongoing_projects,
            'completed_projects': completed_projects,
            'total_publications': total_publications,
            'total_niih_bulletins': total_niih_bulletins,
            'total_bgrc_newsletters': total_bgrc_newsletters,
            'total_awards': total_awards,
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

# Support Department pages
def all_support_departments(request):
    if 'user' in request.session:
        supp_dept_info = support_department.objects.values()
        return render(request, 'admin_dashboard/all_support_departments.html',{'all_supp_dept':supp_dept_info, 'username': request.session['user']})
    return redirect('login')

def add_support_department_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            sup_dept_info = support_department(
                support_department_id = request.POST.get('support_department_id'),
                support_department_name = request.POST.get('support_department_name'),
                support_hod_name = request.POST.get('support_hod_name')            
            )
            sup_dept_info.save()
            messages.success(request, 'Support Department Information Added Successfully')
            return redirect('all_support_departments')
        return render(request, 'admin_dashboard/add_support_department_info.html',{'username': request.session['user']})
    return redirect('login')

def update_support_department_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                # print(request.POST.get('category_name'))
                support_department.objects.filter(support_department_id=request.POST.get('support_department_id')).update(
                    support_department_name=request.POST.get('support_department_name'),
                    support_hod_name=request.POST.get('support_hod_name')
                )
                supp_dept_info = support_department.objects.values()
                return render(request, 'admin_dashboard/all_support_departments.html', {'all_supp_dept': supp_dept_info})

            update_support_department = support_department.objects.filter(support_department_id=request.POST.get('support_department_id')).values()
            param={'update_data':update_support_department,'username': request.session['user']}
            print(update_support_department)
            return render(request, 'admin_dashboard/update_support_department_info.html', param)
            # category.objects.filter(id=request.post.get('id')).update()
        return render(request, 'admin_dashboard/update_support_department_info.html')
    return redirect('login')

def delete_support_department(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('delete_data') == 'delete_data':
                support_department.objects.filter(support_department_id=request.POST.get('support_department_id')).delete()
                supp_dept_info = support_department.objects.values()
                return render(request, 'admin_dashboard/all_support_departments.html', {'all_supp_dept': supp_dept_info, 'username': request.session['user']})

        return render(request, 'admin_dashboard/delete_support_department.html', {'username': request.session['user']})

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
                    orcid = request.POST.get('orcid'),
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
                    orcid = request.POST.get('orcid'),
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
                    
                    profilepic = scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/scientists/"+str(profilepic[0][0])))
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
                        orcid = request.POST.get('orcid'),
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
                        orcid = request.POST.get('orcid'),
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
                    profilepic = scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/scientists/"+str(profilepic[0][0])))
                    scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).delete()
                    all_scientist = scientific_staff.objects.values()
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': all_scientist,'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_scientist.html', {'username': request.session['user']})

# Admin Staff
def all_admin_staff(request):
    if 'user' in request.session:
        all_admins = administration_staff.objects.values()
        return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': all_admins,'username': request.session['user'] })
    return redirect('login')

def add_admin_info(request):
    if 'user' in request.session:
        support_department_name = support_department.objects.values_list('support_department_name')
        category_name = category.objects.filter(category_name = 'Admin').values_list('category_name')
        dropdesig = staff_designation.objects.filter(category_name = 'Admin').values_list('designation')
        param={'category_name':category_name,'dropdesig':dropdesig, 'support_department_name': support_department_name,'username': request.session['user']}
        if request.method == 'POST':
            if request.FILES.get('profilepic_name'):
                fs = FileSystemStorage(location="application/static/dist/images/staff/administration")
                photo=request.FILES['profilepic_name']
                photo = fs.save(photo.name, photo)
                
                uploaded_photo = fs.url(photo).replace('/media/','').replace('%20',' ')
                print(dropdesig)
                print("----------------------------------------------")
                admin_info = administration_staff(
                    admin_id = request.POST.get('admin_id'),
                    admin_name = request.POST.get('admin_name'),
                    support_department_name = request.POST.get('support_department_name'),
                    category_name = request.POST.get('category_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    phone_no = request.POST.get('phone_no'),
                    alt_phone_no = request.POST.get('alt_phone_no'),
                    aadhar_no = request.POST.get('aadhar_no'),
                    fax_no = request.POST.get('fax_no'),
                    profile_status = request.POST.get('profile_status'),
                    level_no = request.POST.get('level_no'),
                    join_year = request.POST.get('join_year'),
                    profilepic_name = uploaded_photo,
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                admin_info.save()
                return redirect('all_admin_staff')
            else:
                admin_info = administration_staff(
                    admin_id = request.POST.get('admin_id'),
                    admin_name = request.POST.get('admin_name'),
                    support_department_name = request.POST.get('support_department_name'),
                    category_name = request.POST.get('category_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    phone_no = request.POST.get('phone_no'),
                    alt_phone_no = request.POST.get('alt_phone_no'),
                    fax_no = request.POST.get('fax_no'),
                    level_no = request.POST.get('level_no'),
                    aadhar_no = request.POST.get('aadhar_no'),
                    join_year = request.POST.get('join_year'),
                    profile_status = request.POST.get('profile_status'),
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                admin_info.save()
                return redirect('all_admin_staff')
        return render(request, 'admin_dashboard/add_admin_info.html', param)
    return redirect('login')

def update_admin_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            #print(request.FILES['profilepic_name'],request.POST.get['profilepic_name'])
            if request.POST.get('update_data') == 'update_data':
                if request.FILES.get('profilepic_name'):
                    fs = FileSystemStorage(location="application/static/dist/images/staff/administration")
                    photo = request.FILES['profilepic_name']
                    photo = fs.save(photo.name, photo)
                    uploaded_photo = fs.url(photo).replace('/media/', '').replace('%20', ' ')

                    profilepic = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/administration/"+str(profilepic[0][0])))
                    administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).update(
                        profilepic_name = uploaded_photo,
                        admin_name = request.POST.get('admin_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_admins = administration_staff.objects.values()
                    return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': all_admins})
                else:
                    administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).update(
                        admin_name = request.POST.get('admin_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_admins = administration_staff.objects.values()
                    return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': all_admins})
            
            update_admin = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values()
            support_department_name = support_department.objects.values_list('support_department_name')
            category_name = category.objects.filter(category_name = 'Admin').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Admin').values_list('designation')
            level=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
            param = {'update_data':update_admin,'dropdesig':dropdesig, 'support_department_name':support_department_name, 'category_name':category_name,'level':level,'username': request.session['user']}
            
            return render(request, 'admin_dashboard/update_admin_info.html',param)
        return render(request, 'admin_dashboard/update_admin_info.html')
    return redirect('login')

def delete_admin(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    profilepic = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/administration/"+str(profilepic[0][0])))
                    administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).delete()
                    all_admins = administration_staff.objects.values()
                    return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': all_admins,'username': request.session['user']})
        # return render(request, 'admin_dashboard/delete_admin.html', {'username': request.session['user']})

# Technical Staff   
def all_technical_staff(request):
    if 'user' in request.session:
        all_technical = technical_staff.objects.values()
        return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': all_technical, 'username': request.session['user']})
    return redirect('login')

def add_technical_info(request):
    if 'user' in request.session:
        support_department_name = support_department.objects.values_list('support_department_name')
        category_name = category.objects.filter(category_name = 'Technical').values_list('category_name')
        dropdesig = staff_designation.objects.filter(category_name = 'Technical').values_list('designation')
        param={'category_name':category_name,'dropdesig':dropdesig, 'support_department_name': support_department_name,'username': request.session['user']}
        if request.method == 'POST':
            if request.FILES.get('profilepic_name'):
                fs = FileSystemStorage(location="application/static/dist/images/staff/technical")
                photo=request.FILES['profilepic_name']
                photo = fs.save(photo.name, photo)
                
                uploaded_photo = fs.url(photo).replace('/media/','').replace('%20',' ')
                print(dropdesig)
                print("----------------------------------------------")
                tech_info = technical_staff(
                    technical_id = request.POST.get('technical_id'),
                    technical_name = request.POST.get('technical_name'),
                    support_department_name = request.POST.get('support_department_name'),
                    category_name = request.POST.get('category_name'),
                    designation = request.POST.get('designation'),
                    email_id = request.POST.get('email_id'),
                    alt_email_id = request.POST.get('alt_email_id'),
                    author_name = request.POST.get('author_name'),
                    phone_no = request.POST.get('phone_no'),
                    alt_phone_no = request.POST.get('alt_phone_no'),
                    aadhar_no = request.POST.get('aadhar_no'),
                    fax_no = request.POST.get('fax_no'),
                    profile_status = request.POST.get('profile_status'),
                    level_no = request.POST.get('level_no'),
                    join_year = request.POST.get('join_year'),
                    profilepic_name = uploaded_photo,
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                tech_info.save()
                return redirect('all_technical_staff')
            else:
                tech_info = technical_staff(
                    technical_id = request.POST.get('technical_id'),
                    technical_name = request.POST.get('technical_name'),
                    support_department_name = request.POST.get('support_department_name'),
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
                    join_year = request.POST.get('join_year'),
                    profile_status = request.POST.get('profile_status'),
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    data_created = datetime.datetime.now()
                )
                tech_info.save()
                return redirect('all_technical_staff')
        return render(request, 'admin_dashboard/add_technical_info.html', param)
    return redirect('login')

def update_technical_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            #print(request.FILES['profilepic_name'],request.POST.get['profilepic_name'])
            if request.POST.get('update_data') == 'update_data':
                if request.FILES.get('profilepic_name'):
                    fs = FileSystemStorage(location="application/static/dist/images/staff/technical")
                    photo = request.FILES['profilepic_name']
                    photo = fs.save(photo.name, photo)
                    uploaded_photo = fs.url(photo).replace('/media/', '').replace('%20', ' ')

                    profilepic = administration_staff.objects.filter(technical_id = request.POST.get('technical_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/technical/"+str(profilepic[0][0])))
                    technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).update(
                        profilepic_name = uploaded_photo,
                        technical_name = request.POST.get('technical_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        author_name = request.POST.get('author_name'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_technical = technical_staff.objects.values()
                    return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': all_technical})
                else:
                    technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).update(
                        technical_name = request.POST.get('technical_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        category_name = request.POST.get('category_name'),
                        designation = request.POST.get('designation'),
                        email_id = request.POST.get('email_id'),
                        alt_email_id = request.POST.get('alt_email_id'),
                        author_name = request.POST.get('author_name'),
                        phone_no = request.POST.get('phone_no'),
                        alt_phone_no = request.POST.get('alt_phone_no'),
                        aadhar_no = request.POST.get('aadhar_no'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        join_year = request.POST.get('join_year'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_technical = technical_staff.objects.values()
                    return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': all_technical})
            
            update_technical = technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).values()
            support_department_name = support_department.objects.values_list('support_department_name')
            category_name = category.objects.filter(category_name = 'Technical').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Technical').values_list('designation')
            level=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
            param = {'update_data':update_technical,'dropdesig':dropdesig, 'support_department_name':support_department_name, 'category_name':category_name,'level':level,'username': request.session['user']}
            print(update_technical)
            return render(request, 'admin_dashboard/update_technical_info.html',param)
        return render(request, 'admin_dashboard/update_technical_info.html')
    return redirect('login')

def delete_technical(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    profilepic = administration_staff.objects.filter(technical_id = request.POST.get('technical_id')).values_list('profilepic_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/technical/"+str(profilepic[0][0])))
                    technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).delete()
                    all_technical = technical_staff.objects.values()
                    return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': all_technical,'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_technical.html',{'username': request.session['user']})

# Project Staff
def all_project_staff(request):
    if 'user' in request.session:
        allproject_staff = project_staff.objects.values()
        return render(request, 'admin_dashboard/all_project_staff.html', {'all_proj_staff': allproject_staff,'username': request.session['user'] })
    return redirect('login')

def add_project_staff_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            proj_staff_info = project_staff(
                project_staff_id = request.POST.get('project_staff_id'),
                project_staff_name = request.POST.get('project_staff_name'),
                project_staff_department = request.POST.get('project_staff_department'),
                project_staff_designation = request.POST.get('project_staff_designation'),
                profile_status = request.POST.get('profile_status')
            )
            proj_staff_info.save()
            return redirect('all_project_staff')
        return render(request, 'admin_dashboard/add_project_staff_info.html', {'username': request.session['user'] })
    return redirect('login')

def update_project_staff_info(request):
    if 'user' in request.session: 
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                project_staff.objects.filter(project_staff_id = request.POST.get('project_staff_id')).update(
                    project_staff_name = request.POST.get('project_staff_name'),
                    project_staff_department = request.POST.get('project_staff_department'),
                    project_staff_designation = request.POST.get('project_staff_designation'),
                    profile_status = request.POST.get('profile_status')
                )
                return redirect('all_project_staff')
            update_proj_staff= project_staff.objects.filter(project_staff_id=request.POST.get('project_staff_id')).values()
        return render(request, 'admin_dashboard/update_project_staff_info.html', {'update_data':update_proj_staff,'username': request.session['user'] })
    return redirect('login')

def delete_project_staff(request):
    if 'user' in request.session:
        all_staff = project_staff.objects.values()
        return render(request, 'admin_dashboard/delete_project_staff.html', {'project_staff': all_staff,'username': request.session['user'] })
    return redirect('login')

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
        category_name = category.objects.values_list('category_name')
        param={'category_name':category_name, 'scientist_name':scientist_name, 'username': request.session['user']}
        if request.method == 'POST':
            project_data = projects(
                project_id = request.POST.get('project_id'),
                project_title = request.POST.get('project_title'),
                scientist_name = request.POST.get('scientist_name'),
                category_name = request.POST.get('category_name'),
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


# Project Pages
def all_publications(request):
    if 'user' in request.session:
        all_publication = publications_list.objects.values()
        return render(request, 'admin_dashboard/all_publications.html',{ 'all_publications':all_publication, 'username': request.session['user'] })
    return redirect('login')

def add_publication_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # Create the new publication object
            publication_data = publications_list(
                publication_id = request.POST.get('publication_id'),
                publication_author_name = request.POST.get('publication_author_name'),
                publication_title = request.POST.get('publication_title'),
                publication_journal_name = request.POST.get('publication_journal_name'),
                publication_type = request.POST.get('publication_type'),
                publication_status = request.POST.get('publication_status'),
                publication_date = request.POST.get('publication_date')
            )
            publication_data.save()
            messages.success(request, 'Publication added successfully!')
            return redirect('all_publications')  
        return render(request, 'admin_dashboard/add_publication_info.html', {'username': request.session['user']})
    return redirect('login')

def update_publication_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                publications_list.objects.filter(publication_id = request.POST.get('publication_id')).update(
                    publication_author_name = request.POST.get('publication_author_name'),
                    publication_title = request.POST.get('publication_title'),
                    publication_journal_name = request.POST.get('publication_journal_name'),
                    publication_type = request.POST.get('publication_type'),
                    publication_status = request.POST.get('publication_status'),
                    publication_date = request.POST.get('publication_date')
                )
                return redirect('all_publications')
            
            update_publication= publications_list.objects.filter(publication_id=request.POST.get('publication_id')).values()
            param={'update_data':update_publication, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_publication_info.html', param)
    return redirect('login')

def delete_publication(request):
    if 'user' in request.session:
        if request.method == 'POST':
            publications_list.objects.filter(publication_id = request.POST.get('publication_id')).delete()
            return redirect('all_publications')
        return render(request, 'admin_dashboard/delete_publication.html', {'username': request.session['user']})

def all_niih_bulletins(request):
    if 'user' in request.session:
        all_niih_bulletins = bulletin_list.objects.values()
        return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':all_niih_bulletins, 'username': request.session['user'] })
    return redirect('login')

def add_niih_bulletin_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.FILES.get('bulletin_file_name'):
                fs = FileSystemStorage(location="application/static/uploads/Bulletins")
                bulletin_file = request.FILES['bulletin_file_name']
                filename = fs.save(bulletin_file.name, bulletin_file)
                uploaded_bulletin_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                
                bulletin_data = bulletin_list(
                    bulletin_id=request.POST.get('bulletin_id'),
                    bulletin_title=request.POST.get('bulletin_title'),
                    bulletin_vol_no=request.POST.get('bulletin_vol_no'),
                    bulletin_year=request.POST.get('bulletin_year'),
                    bulletin_month=request.POST.get('bulletin_month'),
                    bulletin_file_name=uploaded_bulletin_file, 
                )
                bulletin_data.save()
                messages.success(request, 'Bulletin added successfully!')
                return redirect('all_niih_bulletins')
            else:
                bulletin_data = bulletin_list(
                    bulletin_id=request.POST.get('bulletin_id'),
                    bulletin_title=request.POST.get('bulletin_title'),
                    bulletin_vol_no=request.POST.get('bulletin_vol_no'),
                    bulletin_year=request.POST.get('bulletin_year'),
                    bulletin_month=request.POST.get('bulletin_month')
                )
                bulletin_data.save()
                messages.success(request, 'Bulletin added successfully!')
                return redirect('all_niih_bulletins')
        return render(request, 'admin_dashboard/add_niih_bulletin_info.html', {'username': request.session['user']})
    return redirect('login')

def update_niih_bulletin_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print("\n-----------------------------------")
                if request.FILES.get('bulletin_file_name'):
                    print("\n-----------------------------------")
                    fs = FileSystemStorage(location="application/static/uploads/Bulletins")
                    bulletin_file = request.FILES['bulletin_file_name']
                    filename = fs.save(bulletin_file.name, bulletin_file)
                    uploaded_bulletin_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                    bulletin_file = bulletin_list.objects.filter(bulletin_id = request.POST.get('bulletin_id')).values_list('bulletin_file_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Bulletins/"+str(bulletin_file[0][0])))
                    
                    bulletin_list.objects.filter(bulletin_id=request.POST.get('bulletin_id')).update(
                        bulletin_title=request.POST.get('bulletin_title'),
                        bulletin_vol_no=request.POST.get('bulletin_vol_no'),
                        bulletin_year=request.POST.get('bulletin_year'),
                        bulletin_month=request.POST.get('bulletin_month'),
                        bulletin_file_name=uploaded_bulletin_file, 
                    )
                    all_niih_bulletins = bulletin_list.objects.values()
                    messages.success(request, 'Bulletin update successfully!')
                    return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':all_niih_bulletins})
                else:
                    bulletin_list.objects.filter(bulletin_id=request.POST.get('bulletin_id')).update(
                        bulletin_title=request.POST.get('bulletin_title'),
                        bulletin_vol_no=request.POST.get('bulletin_vol_no'),
                        bulletin_year=request.POST.get('bulletin_year'),
                        bulletin_month=request.POST.get('bulletin_month')
                    )
                    all_niih_bulletins = bulletin_list.objects.values()
                    messages.success(request, 'Bulletin update successfully!')
                    return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':all_niih_bulletins})
            update_bulletins = bulletin_list.objects.filter(bulletin_id = request.POST.get('bulletin_id')).values()
            param = {'update_data':update_bulletins,'username': request.session['user']}
            print(update_bulletins)
        return render(request, 'admin_dashboard/update_niih_bulletin_info.html', param)
    return redirect('login')

def delete_niih_bulletin(request):
    if 'user' in request.session:
        if request.method == 'POST':
            bulletin_file = bulletin_list.objects.filter(bulletin_id = request.POST.get('bulletin_id')).values_list('bulletin_file_name')
            print(bulletin_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Bulletins/"+str(bulletin_file[0][0])))
            bulletin_list.objects.filter(bulletin_id = request.POST.get('bulletin_id')).delete()
            return redirect('all_niih_bulletins')
        return render(request, 'admin_dashboard/delete_niih_bulletin.html', {'username': request.session['user']})
    
def all_newsletters(request):
    if 'user' in request.session:
        all_newsletter = newsletter_list.objects.values()
        return render(request, 'admin_dashboard/all_newsletters.html',{ 'all_news':all_newsletter, 'username': request.session['user'] })
    return redirect('login')  
  
def add_newsletter_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # Create the new publication object
            newsletter_data = newsletter_list(
                newsletter_id=request.POST.get('newsletter_id'),
                newsletter_title=request.POST.get('newsletter_title'),
                newsletter_vol_no=request.POST.get('newsletter_vol_no'),
                newsletter_year=request.POST.get('newsletter_year'),
                newsletter_month=request.POST.get('newsletter_month')
            )
            newsletter_data.save()
            messages.success(request, 'Newsletter added successfully!')
            return redirect('all_newsletters')
        return render(request, 'admin_dashboard/add_newsletter_info.html',{ 'username': request.session['user'] })
    return redirect('login')   
 
def update_newsletter_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                newsletter_list.objects.filter(newsletter_id = request.POST.get('newsletter_id')).update(
                    newsletter_title=request.POST.get('newsletter_title'),
                    newsletter_vol_no=request.POST.get('newsletter_vol_no'),
                    newsletter_year=request.POST.get('newsletter_year'),
                    newsletter_month=request.POST.get('newsletter_month')
                )
                return redirect('all_newsletters')
            
            update_newsletter= newsletter_list.objects.filter(newsletter_id=request.POST.get('newsletter_id')).values()
            param={'update_data':update_newsletter, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_newsletter_info.html', param)
    return redirect('login')    

def delete_newsletter(request):
    if 'user' in request.session:
        return render(request, 'admin_dashboard/delete_newsletter.html',{ 'all_bulletins':all_niih_bulletins, 'username': request.session['user'] })


def all_awards(request):
    if 'user' in request.session:
        all_awards_list = award_list.objects.values()
        return render(request, 'admin_dashboard/all_awards.html',{ 'all_awards':all_awards_list, 'username': request.session['user'] })
    return redirect('login')

def add_award_info(request):
    if 'user' in request.session:
        scientist_name = scientific_staff.objects.values_list('scientist_name')
        param={'scientist_name':scientist_name,'username': request.session['user']}
        print(scientist_name)
        if request.method == 'POST':
            award_data = award_list(
                award_name = request.POST.get('award_name'),
                scientist_name = request.POST.get('scientist_name')
            )
            award_data.save()
            return redirect('all_awards')
        return render(request, 'admin_dashboard/add_award_info.html', param)
    return redirect('login')

def update_award_info(request):
    if 'user' in request.session:
        scientist_name = scientific_staff.objects.values_list('scientist_name')
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print(request.POST.get('award_name'),request.POST.get('scientist_name'))
                award_list.objects.filter(scientist_name=request.POST.get('scientist_name')).update(
                    award_name = request.POST.get('award_name'),
                    scientist_name = request.POST.get('scientist_name')
                )
                return redirect('all_awards')
        award_detail = award_list.objects.filter(award_name = request.POST.get('award_name')).values()
        return render(request, 'admin_dashboard/update_award_info.html', {'update_data': award_detail, 'scientist_name': scientist_name,'username': request.session['user']})
    return redirect('login')

def delete_award(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('delete_data') == 'delete_data':
                award_list.objects.filter(award_name=request.POST.get('award_name')).delete()
                all_awards_list = award_list.objects.values()
                return render(request, 'admin_dashboard/all_awards.html', { 'all_awards':all_awards_list, 'username': request.session['user']})
        return render(request, 'admin_dashboard/delete_award.html',{ 'username': request.session['user'] })

