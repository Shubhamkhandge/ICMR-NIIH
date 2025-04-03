import datetime
import os
from django.core.paginator import Paginator
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
        total_scientist_staff = scientific_staff.objects.count()
        total_admin_staff = administration_staff.objects.count()
        total_technical_staff = technical_staff.objects.count()
        total_project_staff = project_staff.objects.count()
        total_student_staff = student_staff.objects.count()
        total_alumini_staff = alumini_staff.objects.count()
        total_projects = projects.objects.count()
        total_publications = publications_list.objects.count()
        total_niih_bulletins = bulletin_list.objects.count()
        total_bgrc_newsletters = newsletter_list.objects.count()
        total_circulars = circular_list.objects.count()
        total_advertises = advertise_list.objects.count()
        total_tenders = tender_list.objects.count()
        total_awards = award_list.objects.count()
        total_event = media.objects.count()

        # Assuming 'project_status' field to differentiate between ongoing and completed projects
        ongoing_projects = projects.objects.filter(project_status='on going').count()
        completed_projects = projects.objects.filter(project_status='completed').count()

        context = {
            'username': request.session['user'],
            'total_departments': total_departments,
            'total_support_departments': total_support_departments,
            'total_categories': total_categories,
            'total_designations': total_designations,
            'total_scientist_staff': total_scientist_staff,
            'total_admin_staff': total_admin_staff,
            'total_technical_staff': total_technical_staff,
            'total_project_staff': total_project_staff,
            'total_student_staff': total_student_staff,
            'total_alumini_staff': total_alumini_staff,
            'total_projects': total_projects,
            'ongoing_projects': ongoing_projects,
            'completed_projects': completed_projects,
            'total_publications': total_publications,
            'total_niih_bulletins': total_niih_bulletins,
            'total_bgrc_newsletters': total_bgrc_newsletters,
            'total_circulars': total_circulars,
            'total_advertises': total_advertises,
            'total_tenders': total_tenders,
            'total_awards': total_awards,
            'total_event': total_event,
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
        paginator = Paginator(supp_dept_info, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_support_departments.html',{'all_supp_dept':page_obj, 'username': request.session['user']})
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
        paginator = Paginator(all_desig, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_designations.html', {'all_designation': page_obj, 'username': request.session['user']})
    return redirect('login')

def add_designation_info(request):
    if 'user' in request.session:
        category_name = category.objects.values_list('category_name')
        support_department_name = support_department.objects.values_list('support_department_name')
        # lab_department_name = dept_info.objects.values_list('lab_department_name')
        param={'category_name':category_name,'support_department_name':support_department_name,'username': request.session['user']}
        print(category_name)
        if request.method == 'POST':
            desig_name = request.POST.get('designation')
            cat_name = request.POST.get('category_name')
            supp_name = request.POST.get('support_department_name')

            print(staff_designation.objects.filter(designation = desig_name, category_name = cat_name).values_list())
            if not staff_designation.objects.filter(designation = desig_name, category_name = cat_name, support_department_name = supp_name).exists():
                desig = staff_designation(
                    designation = desig_name,
                    category_name = cat_name,
                    support_department_name = supp_name
                )
                desig.save()
            return redirect('all_designations')
        return render(request, 'admin_dashboard/add_designation_info.html', param)
    return redirect('login')
                  
def update_designation_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print(request.POST.get('designation'),request.POST.get('category_name'))  # Debugging to check what you're getting

                staff_designation.objects.filter(id=request.POST.get('id')).update(
                    designation = request.POST.get('designation'),
                    category_name = request.POST.get('category_name'),
                    support_department_name = request.POST.get('support_department_name'),
                )
                return redirect('all_designations')

            update_designation = staff_designation.objects.filter(designation=request.POST.get('designation')).values()
            category_name = category.objects.values_list('category_name')  # This line fetches the categories (if needed for dropdown or display)
            support_department_name = support_department.objects.values_list('support_department_name')
           
            return render(request, 'admin_dashboard/update_designation_info.html', {
                'update_data': update_designation,
                'support_department_name': support_department_name,
                'category_name': category_name,  # Ensure this is passed here
                'username': request.session['user']
            })

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
        paginator = Paginator(all_scientist, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': page_obj, 'username': request.session['user']})
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
                    div_name = request.POST.get('div_name'),
                    # guide_name = request.POST.get('guide_name'),
                    fax_no = request.POST.get('fax_no'),
                    profile_status = request.POST.get('profile_status'),
                    level_no = request.POST.get('level_no'),
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    join_date = request.POST.get('join_date'),
                    retire_date = request.POST.get('retire_date'),
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
                    div_name = request.POST.get('div_name'),
                    # guide_name = request.POST.get('guide_name'),
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    join_date = request.POST.get('join_date'),
                    retire_date = request.POST.get('retire_date'),
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
                        orcid = request.POST.get('orcid'),
                        div_name = request.POST.get('div_name'),
                        # guide_name = request.POST.get('guide_name'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        birth_date = request.POST.get('birth_date'),
                        current_post_date = request.POST.get('current_post_date'),
                        join_date = request.POST.get('join_date'),
                        retire_date = request.POST.get('retire_date'),
                        research_interests = request.POST.get('research_interests'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_scientist = scientific_staff.objects.values()
                    paginator = Paginator(all_scientist, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': page_obj,'username': request.session['user']})
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
                        div_name = request.POST.get('div_name'),
                        # guide_name = request.POST.get('guide_name'),
                        fax_no = request.POST.get('fax_no'),
                        profile_status = request.POST.get('profile_status'),
                        level_no = request.POST.get('level_no'),
                        birth_date = request.POST.get('birth_date'),
                        current_post_date = request.POST.get('current_post_date'),
                        join_date = request.POST.get('join_date'),
                        retire_date = request.POST.get('retire_date'),
                        research_interests = request.POST.get('research_interests'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_scientist = scientific_staff.objects.values()
                    paginator = Paginator(all_scientist, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_scientists_staff.html', {'all_sci': page_obj,'username': request.session['user']})
            update_scientist = scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).values()
            lab_department_name = dept_info.objects.values_list('lab_department_name')
            category_name = category.objects.filter(category_name = 'Scientist').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Scientist').values_list('designation')
            level=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,'13A',14]
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
                    if str(profilepic[0][0]) != 'None':
                        os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/scientists/"+str(profilepic[0][0])))
                        scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).delete()
                        return redirect('all_scientists_staff')
                    else:
                        scientific_staff.objects.filter(scientist_id = request.POST.get('scientist_id')).delete()
                        return redirect('all_scientists_staff')
        return redirect('all_scientists_staff')
    return redirect('login')

# Admin Staff
def all_admin_staff(request):
    if 'user' in request.session:
        all_admins = administration_staff.objects.values()
        paginator = Paginator(all_admins, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': page_obj,'username': request.session['user'] })
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
                    div_name = request.POST.get('div_name'),
                    level_no = request.POST.get('level_no'),
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    retire_date = request.POST.get('retire_date'),
                    join_date = request.POST.get('join_date'),
                    profilepic_name = uploaded_photo,
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    display_order = request.POST.get('display_order'),
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
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    retire_date = request.POST.get('retire_date'),
                    join_date = request.POST.get('join_date'),
                    profile_status = request.POST.get('profile_status'),
                    div_name = request.POST.get('div_name'),
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    display_order = request.POST.get('display_order'),
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
                    photo=request.FILES['profilepic_name']
                    photo = fs.save(photo.name, photo)
                    
                    uploaded_photo = fs.url(photo).replace('/media/','').replace('%20',' ')
                    
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
                    div_name = request.POST.get('div_name'),
                    level_no = request.POST.get('level_no'),
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    retire_date = request.POST.get('retire_date'),
                    join_date = request.POST.get('join_date'),
                    specialization = request.POST.get('specialization'),
                    academic_background = request.POST.get('academic_background'),
                    professional_experience = request.POST.get('professional_experience'),
                    display_order = request.POST.get('display_order'),
                    data_created = datetime.datetime.now()
                    )
                    all_admins = administration_staff.objects.values()
                    paginator = Paginator(all_admins, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': page_obj,'username': request.session['user']})
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
                        div_name = request.POST.get('div_name'),
                        level_no = request.POST.get('level_no'),
                        birth_date = request.POST.get('birth_date'),
                        current_post_date = request.POST.get('current_post_date'),
                        retire_date = request.POST.get('retire_date'),
                        join_date = request.POST.get('join_date'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        display_order = request.POST.get('display_order'),
                        data_created = datetime.datetime.now()
                    )
                    all_admins = administration_staff.objects.values()
                    paginator = Paginator(all_admins, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_admin_staff.html', {'all_admin': page_obj,'username': request.session['user']})
            
            update_admin = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values()
            support_department_name = support_department.objects.values_list('support_department_name')
            category_name = category.objects.filter(category_name = 'Admin').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Admin').values_list('designation')
            level=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,'13A',14]
            display_order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            param = {'update_data':update_admin,'dropdesig':dropdesig, 'support_department_name':support_department_name, 'category_name':category_name,'level':level,'display_order':display_order,'username': request.session['user']}
            
            return render(request, 'admin_dashboard/update_admin_info.html',param)
        return render(request, 'admin_dashboard/update_admin_info.html')
    return redirect('login')

def delete_admin(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    profilepic = administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).values_list('profilepic_name')   
                    if profilepic[0][0] != 'None':
                        os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/administration/"+str(profilepic[0][0])))
                        administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).delete()
                        return redirect('all_admin_staff')
                    else:
                        administration_staff.objects.filter(admin_id = request.POST.get('admin_id')).delete()
                        return redirect('all_admin_staff')
            
        
        # return render(request, 'admin_dashboard/delete_admin.html', {'username': request.session['user']})

# Technical Staff   
def all_technical_staff(request):
    if 'user' in request.session:
        all_technical = technical_staff.objects.values()
        paginator = Paginator(all_technical, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': page_obj, 'username': request.session['user']})
    return redirect('login')

def add_technical_info(request):
    if 'user' in request.session:
        lab_department_name = dept_info.objects.values_list('lab_department_name')
        support_department_name = support_department.objects.values_list('support_department_name')
        category_name = category.objects.filter(category_name = 'Technical').values_list('category_name')
        dropdesig = staff_designation.objects.filter(category_name = 'Technical').values_list('designation')
        param={'category_name':category_name,'dropdesig':dropdesig, 'support_department_name': support_department_name, 'lab_department_name': lab_department_name ,'username': request.session['user']}
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
                    lab_department_name = request.POST.get('lab_department_name'),
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
                    div_name = request.POST.get('div_name'),
                    level_no = request.POST.get('level_no'),
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    retire_date = request.POST.get('retire_date'),
                    join_date = request.POST.get('join_date'),
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
                    birth_date = request.POST.get('birth_date'),
                    current_post_date = request.POST.get('current_post_date'),
                    retire_date = request.POST.get('retire_date'),
                    join_date = request.POST.get('join_date'),
                    profile_status = request.POST.get('profile_status'),
                    div_name = request.POST.get('div_name'),
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

                    
                    technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).update(
                        technical_id = request.POST.get('technical_id'),
                        profilepic_name = uploaded_photo,
                        technical_name = request.POST.get('technical_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        lab_department_name = request.POST.get('lab_department_name'),
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
                        div_name = request.POST.get('div_name'),
                        level_no = request.POST.get('level_no'),
                        birth_date = request.POST.get('birth_date'),
                        current_post_date = request.POST.get('current_post_date'),
                        retire_date = request.POST.get('retire_date'),
                        join_date = request.POST.get('join_date'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_technical = technical_staff.objects.values()
                    paginator = Paginator(all_technical, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': page_obj,'username': request.session['user']})
                else:
                    technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).update(
                        technical_id = request.POST.get('technical_id'),
                        technical_name = request.POST.get('technical_name'),
                        support_department_name = request.POST.get('support_department_name'),
                        lab_department_name = request.POST.get('lab_department_name'),
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
                        div_name = request.POST.get('div_name'),
                        level_no = request.POST.get('level_no'),
                        birth_date = request.POST.get('birth_date'),
                        current_post_date = request.POST.get('current_post_date'),
                        retire_date = request.POST.get('retire_date'),
                        join_date = request.POST.get('join_date'),
                        specialization = request.POST.get('specialization'),
                        academic_background = request.POST.get('academic_background'),
                        professional_experience = request.POST.get('professional_experience'),
                        data_created = datetime.datetime.now()
                    )
                    all_technical = technical_staff.objects.values()
                    paginator = Paginator(all_technical, 10)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'admin_dashboard/all_technical_staff.html', {'all_tech': page_obj,'username': request.session['user']})
            
            update_technical = technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).values()
            lab_department_name = dept_info.objects.values_list('lab_department_name')
            support_department_name = support_department.objects.values_list('support_department_name')
            category_name = category.objects.filter(category_name = 'Technical').values_list('category_name')
            dropdesig = staff_designation.objects.filter(category_name = 'Technical').values_list('designation')
            level=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,'13A',14]
            param = {'update_data':update_technical,'dropdesig':dropdesig, 'support_department_name':support_department_name, 'lab_department_name': lab_department_name, 'category_name':category_name,'level':level,'username': request.session['user']}
            print(update_technical)
            return render(request, 'admin_dashboard/update_technical_info.html',param)
        return render(request, 'admin_dashboard/update_technical_info.html')
    return redirect('login')

def delete_technical(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).exists():
                if request.POST.get('delete_data') == 'delete_data':
                    profilepic = technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).values_list('profilepic_name')
                    if profilepic[0][0] != "None":
                        os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/dist/images/staff/technical/"+str(profilepic[0][0])))
                        return redirect('all_technical_staff')
                    else:
                        technical_staff.objects.filter(technical_id = request.POST.get('technical_id')).delete()
                        return redirect('all_technical_staff')
        return redirect('all_technical_staff')

# Project Staff
def all_project_staff(request):
    if 'user' in request.session:
        allproject_staff = project_staff.objects.values()
        paginator = Paginator(allproject_staff, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_project_staff.html', {'all_proj_staff': page_obj,'username': request.session['user'] })
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

# Student Pages
def all_student_staff(request):
    if 'user' in request.session:
        all_students = student_staff.objects.values()
        paginator = Paginator(all_students, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_student_staff.html', {'all_student_info': page_obj, 'username': request.session['user']})
    return redirect('login')

def add_student_staff_info(request):
    if 'user' in request.session:
        lab_department_name = dept_info.objects.values_list('lab_department_name')
        if request.method == 'POST':
            student_data = student_staff(
                student_staff_id = request.POST.get('student_staff_id'),
                student_staff_name = request.POST.get('student_staff_name'),
                student_guide_name = request.POST.get('student_guide_name'),
                # lab_department_name = request.POST.get('lab_department_name'),
                student_staff_department = request.POST.get('student_staff_department'),
                student_join_year = request.POST.get('student_join_year'),
                profile_status = request.POST.get('profile_status')
            )
            student_data.save()
            return redirect('all_student_staff') 
        return render(request, 'admin_dashboard/add_student_staff_info.html', {'lab_department_name': lab_department_name,'username': request.session['user']})
    return redirect('login')

def update_student_staff_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                student_staff.objects.filter(student_staff_id = request.POST.get('student_staff_id')).update(
                    student_staff_id = request.POST.get('student_staff_id'),
                    student_staff_name = request.POST.get('student_staff_name'),
                    student_guide_name = request.POST.get('student_guide_name'),
                    # lab_department_name = request.POST.get('lab_department_name'),
                    student_staff_department = request.POST.get('student_staff_department'),
                    student_join_year = request.POST.get('student_join_year'),
                    profile_status = request.POST.get('profile_status')
                )
                return redirect('all_student_staff')
            
            update_student= student_staff.objects.filter(student_staff_id=request.POST.get('student_staff_id')).values()
            lab_department_name = dept_info.objects.values_list('lab_department_name')
            param={'update_data':update_student, 'lab_department_name': lab_department_name,'username': request.session['user'] }
        return render(request, 'admin_dashboard/update_student_staff_info.html',param)
    return redirect('login')

def delete_student(request):
    if 'user' in request.session:
        if request.method == 'POST':
            student_staff.objects.filter(student_staff_id = request.POST.get('student_staff_id')).delete()
            return redirect('all_student_staff')
        return redirect('all_student')
    return redirect('login')

# Alumini Pages
def all_alumini_staff(request):
    if 'user' in request.session:
        all_aluminis = alumini_staff.objects.values()
        paginator = Paginator(all_aluminis, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_alumini_staff.html', {'all_alumini_info': page_obj, 'username': request.session['user']})
    return redirect('login')

def add_alumini_staff_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            alumini_data = alumini_staff(
                alumini_staff_id = request.POST.get('alumini_staff_id'),
                alumini_staff_name = request.POST.get('alumini_staff_name'),
                alumini_staff_designation = request.POST.get('alumini_staff_designation'),
                alumini_leave_year = request.POST.get('alumini_leave_year'),
                profile_status = request.POST.get('profile_status')
            )
            alumini_data.save()
            return redirect('all_alumini_staff') 
        return render(request, 'admin_dashboard/add_alumini_staff_info.html')
    return redirect('login')

def update_alumini_staff_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                alumini_staff.objects.filter(alumini_staff_id = request.POST.get('alumini_staff_id')).update(
                    alumini_staff_name = request.POST.get('alumini_staff_name'),
                    alumini_staff_designation = request.POST.get('alumini_staff_designation'),
                    alumini_leave_year = request.POST.get('alumini_leave_year'),
                    profile_status = request.POST.get('profile_status')
                )
                return redirect('all_alumini_staff')
            
            update_alumini= alumini_staff.objects.filter(alumini_staff_id=request.POST.get('alumini_staff_id')).values()
            param={'update_data':update_alumini, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_alumini_staff_info.html',param)
    return redirect('login')

def delete_alumini(request):
    if 'user' in request.session:
        if request.method == 'POST':
            alumini_staff.objects.filter(alumini_staff_id = request.POST.get('alumini_staff_id')).delete()
            return redirect('all_alumini_staff')
        return render(request, 'admin_dashboard/delete_alumini.html', {'username': request.session['user']})

# Project Pages
def all_projects(request):
    if 'user' in request.session:
        all_project = projects.objects.values()
        ongoing_project = projects.objects.filter(project_status = 'On going').values()
        paginator = Paginator(ongoing_project, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        completed_project = projects.objects.filter(project_status = 'Completed').values()
        paginator1 = Paginator(completed_project, 10)
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)
        return render(request, 'admin_dashboard/all_projects.html', {'all_project': all_project, 'ongoing_project': page_obj , 'completed_project': page_obj1, 'username': request.session['user']})
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
        return redirect('projects')

# Project Pages
def all_publications(request):
    if 'user' in request.session:
        all_publication = publications_list.objects.values()
        paginator = Paginator(all_publication, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_publications.html',{ 'all_publications':page_obj, 'username': request.session['user'] })
    return redirect('login')

def add_publication_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # Create the new publication object
            publication_data = publications_list(
                # publication_id = request.POST.get('publication_id'),
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
                publications_list.objects.filter(id = request.POST.get('id')).update(
                    publication_author_name = request.POST.get('publication_author_name'),
                    publication_title = request.POST.get('publication_title'),
                    publication_journal_name = request.POST.get('publication_journal_name'),
                    publication_type = request.POST.get('publication_type'),
                    publication_status = request.POST.get('publication_status'),
                    publication_date = request.POST.get('publication_date')
                )
                return redirect('all_publications')
            
            update_publication= publications_list.objects.filter(id=request.POST.get('id')).values()
            param={'update_data':update_publication, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_publication_info.html', param)
    return redirect('login')

def delete_publication(request):
    if 'user' in request.session:
        if request.method == 'POST':
            publications_list.objects.filter(id = request.POST.get('id')).delete()
            return redirect('all_publications')
        return render(request, 'admin_dashboard/delete_publication.html', {'username': request.session['user']})

def all_niih_bulletins(request):
    if 'user' in request.session:
        all_niih_bulletins = bulletin_list.objects.values()
        paginator = Paginator(all_niih_bulletins, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':page_obj, 'username': request.session['user'] })
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
                    # bulletin_id = request.POST.get('bulletin_id'),
                    bulletin_title = request.POST.get('bulletin_title'),
                    bulletin_vol_no = request.POST.get('bulletin_vol_no'),
                    bulletin_year = request.POST.get('bulletin_year'),
                    bulletin_month = request.POST.get('bulletin_month'),
                    bulletin_file_name = uploaded_bulletin_file, 
                )
                bulletin_data.save()
                messages.success(request, 'Bulletin added successfully!')
                return redirect('all_niih_bulletins')
            else:
                bulletin_data = bulletin_list(
                    # bulletin_id = request.POST.get('bulletin_id'),
                    bulletin_title = request.POST.get('bulletin_title'),
                    bulletin_vol_no = request.POST.get('bulletin_vol_no'),
                    bulletin_year = request.POST.get('bulletin_year'),
                    bulletin_month = request.POST.get('bulletin_month')
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
                    
                    bulletin_list.objects.filter(id = request.POST.get('id')).update(
                        bulletin_title = request.POST.get('bulletin_title'),
                        bulletin_vol_no = request.POST.get('bulletin_vol_no'),
                        bulletin_year = request.POST.get('bulletin_year'),
                        bulletin_month = request.POST.get('bulletin_month'),
                        bulletin_file_name = uploaded_bulletin_file, 
                    )
                    all_niih_bulletins = bulletin_list.objects.values()
                    messages.success(request, 'Bulletin update successfully!')
                    return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':all_niih_bulletins})
                else:
                    bulletin_list.objects.filter(id = request.POST.get('id')).update(
                        bulletin_title = request.POST.get('bulletin_title'),
                        bulletin_vol_no = request.POST.get('bulletin_vol_no'),
                        bulletin_year = request.POST.get('bulletin_year'),
                        bulletin_month = request.POST.get('bulletin_month')
                    )
                    all_niih_bulletins = bulletin_list.objects.values()
                    messages.success(request, 'Bulletin without file update successfully!')
                    return render(request, 'admin_dashboard/all_niih_bulletins.html',{ 'all_bulletins':all_niih_bulletins})
            update_bulletins = bulletin_list.objects.filter(id = request.POST.get('id')).values()
            param = {'update_data':update_bulletins,'username': request.session['user']}
            print(update_bulletins)
        return render(request, 'admin_dashboard/update_niih_bulletin_info.html', param)
    return redirect('login')

def delete_niih_bulletin(request):
    if 'user' in request.session:
        if request.method == 'POST':
            bulletin_file = bulletin_list.objects.filter(id = request.POST.get('id')).values_list('bulletin_file_name')
            print(bulletin_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Bulletins/"+str(bulletin_file[0][0])))
            bulletin_list.objects.filter(id = request.POST.get('id')).delete()
            return redirect('all_niih_bulletins')
        return render(request, 'admin_dashboard/delete_niih_bulletin.html', {'username': request.session['user']})
    
def all_newsletters(request):
    if 'user' in request.session:
        all_newsletter = newsletter_list.objects.values()
        paginator = Paginator(all_newsletter, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_newsletters.html',{ 'all_news':page_obj, 'username': request.session['user'] })
    return redirect('login')  
  
def add_newsletter_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            # Create the new publication object
            newsletter_data = newsletter_list(
                # newsletter_id=request.POST.get('newsletter_id'),
                newsletter_title = request.POST.get('newsletter_title'),
                newsletter_vol_no = request.POST.get('newsletter_vol_no'),
                newsletter_year = request.POST.get('newsletter_year'),
                newsletter_month = request.POST.get('newsletter_month')
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
                newsletter_list.objects.filter(id = request.POST.get('id')).update(
                    newsletter_title = request.POST.get('newsletter_title'),
                    newsletter_vol_no = request.POST.get('newsletter_vol_no'),
                    newsletter_year = request.POST.get('newsletter_year'),
                    newsletter_month = request.POST.get('newsletter_month')
                )
                return redirect('all_newsletters')
            
            update_newsletter= newsletter_list.objects.filter(id = request.POST.get('id')).values()
            param={'update_data':update_newsletter, 'username': request.session['user']}
        return render(request, 'admin_dashboard/update_newsletter_info.html', param)
    return redirect('login')    

def delete_newsletter(request):
    if 'user' in request.session:
        if request.POST.get('delete_data') == 'delete_data':
            newsletter_list.objects.filter(id = request.POST.get('id')).delete()
            all_newsletter = newsletter_list.objects.values()
            return render(request, 'admin_dashboard/all_newsletters.html', { 'all_news':all_newsletter})
        return render(request, 'admin_dashboard/delete_newsletter.html',{ 'username': request.session['user'] })
    return redirect('login')

def all_awards(request):
    if 'user' in request.session:
        all_awards_list = award_list.objects.values()
        paginator = Paginator(all_awards_list, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_awards.html',{ 'all_awards':page_obj, 'username': request.session['user'] })
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
                award_list.objects.filter(id = request.POST.get('id')).update(
                    award_name = request.POST.get('award_name'),
                    scientist_name = request.POST.get('scientist_name')
                )
                return redirect('all_awards')
        award_detail = award_list.objects.filter(id = request.POST.get('id')).values()
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

def all_advertise(request):
    if 'user' in request.session:
        all_advertise = advertise_list.objects.values()
        paginator = Paginator(all_advertise, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_advertise.html',{ 'all_advertise_info':page_obj, 'username': request.session['user'] })
    return redirect('login')

def add_advertise_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.FILES.get('advertise_file_name'):
                fs = FileSystemStorage(location="application/static/uploads/Advertise")
                advertise_file = request.FILES['advertise_file_name']
                filename = fs.save(advertise_file.name, advertise_file)
                uploaded_advertise_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                
                advertise_data = advertise_list(
                    advertise_id = request.POST.get('advertise_id'),
                    advertise_title = request.POST.get('advertise_title'),
                    advertise_date = request.POST.get('advertise_date'),
                    advertise_file_name = uploaded_advertise_file, 
                    advertise_status = request.POST.get('advertise_status'),
                )
                advertise_data.save()
                messages.success(request, 'Advertise added successfully!')
                return redirect('all_advertise')
            else:
                advertise_data  =  advertise_list(
                    advertise_id = request.POST.get('advertise_id'),
                    advertise_title = request.POST.get('advertise_title'),
                    advertise_date = request.POST.get('advertise_date'),
                    advertise_status = request.POST.get('advertise_status'),
                )
                advertise_data.save()
                messages.success(request, 'Advertise added successfully!')
                return redirect('all_advertise')
        return render(request, 'admin_dashboard/add_advertise_info.html', {'username': request.session['user']})
    return redirect('login')

def update_advertise_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print("\n-----------------------------------")
                if request.FILES.get('advertise_file_name'):
                    print("\n-----------------------------------")
                    fs = FileSystemStorage(location="application/static/uploads/Advertise")
                    advertise_file = request.FILES['advertise_file_name']
                    filename = fs.save(advertise_file.name, advertise_file)
                    uploaded_advertise_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                    
                    advertise_file = advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).values_list('advertise_file_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Advertise/"+str(advertise_file[0][0])))
                    
                    advertise_list.objects.filter(advertise_id=request.POST.get('advertise_id')).update(
                        advertise_title=request.POST.get('advertise_title'),
                        advertise_date = request.POST.get('advertise_date'),
                        advertise_file_name = uploaded_advertise_file, 
                        advertise_status = request.POST.get('advertise_status'),
                    )
                    all_advertise = advertise_list.objects.values()
                    messages.success(request, 'Advertise update successfully!')
                    return render(request, 'admin_dashboard/all_advertise.html',{ 'all_advertise_info':all_advertise})
                else:
                    advertise_list.objects.filter(advertise_id=request.POST.get('advertise_id')).update(
                        advertise_title=request.POST.get('advertise_title'),
                        advertise_date = request.POST.get('advertise_date'),
                        advertise_status = request.POST.get('advertise_status'),
                    )
                    all_advertise = advertise_list.objects.values()
                    messages.success(request, 'Advertise update successfully!')
                    return render(request, 'admin_dashboard/all_advertise.html',{ 'all_advertise_info':all_advertise})
            
            update_advertise = advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).values()
            param = {'update_data':update_advertise,'username': request.session['user']}
            print(update_advertise)
        return render(request, 'admin_dashboard/update_advertise_info.html', param)
    return redirect('login')

def delete_advertise(request):
    if 'user' in request.session:
        if request.method == 'POST':
            advertise_file = advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).values_list('advertise_file_name')
            print(advertise_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Advertise/"+str(advertise_file[0][0])))
            advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).delete()
            return redirect('all_advertise')
        return render(request, 'admin_dashboard/delete_advertise.html', {'username': request.session['user']})

def all_circulars(request):
    if 'user' in request.session:
        all_circular = circular_list.objects.values()
        paginator = Paginator(all_circular, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_circulars.html',{ 'all_circular_info':page_obj, 'username': request.session['user'] })
    return redirect('login')

def add_circular_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.FILES.get('circular_file_name'):
                fs = FileSystemStorage(location="application/static/uploads/Circulars")
                circular_file = request.FILES['circular_file_name']
                filename = fs.save(circular_file.name, circular_file)
                uploaded_circular_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                
                circular_data = circular_list(
                    circular_id = request.POST.get('circular_id'),
                    circular_title = request.POST.get('circular_title'),
                    circular_date = request.POST.get('circular_date'),
                    circular_file_name = uploaded_circular_file, 
                    circular_status = request.POST.get('circular_status')
                )
                circular_data.save()
                messages.success(request, 'Circular added successfully!')
                return redirect('all_circulars')
            else:
                circular_data  =  circular_list(
                    circular_id = request.POST.get('circular_id'),
                    circular_title = request.POST.get('circular_title'),
                    circular_date = request.POST.get('circular_date'),
                    circular_status = request.POST.get('circular_status')
                )
                circular_data.save()
                messages.success(request, 'Circular added successfully!')
                return redirect('all_circulars')
        return render(request, 'admin_dashboard/add_circular_info.html', {'username': request.session['user']})
    return redirect('login')

def update_circular_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print("\n-----------------------------------")
                if request.FILES.get('circular_file_name'):
                    print("\n-----------------------------------")
                    fs = FileSystemStorage(location="application/static/uploads/Circulars")
                    circular_file = request.FILES['circular_file_name']
                    filename = fs.save(circular_file.name, circular_file)
                    uploaded_circular_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                    
                    circular_file = circular_list.objects.filter(circular_id = request.POST.get('circular_id')).values_list('circular_file_name')    
                    os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Circulars/"+str(circular_file[0][0])))
                    
                    circular_list.objects.filter(circular_id=request.POST.get('circular_id')).update(
                        circular_title=request.POST.get('circular_title'),
                        circular_date = request.POST.get('circular_date'),
                        circular_file_name = uploaded_circular_file, 
                        circular_status = request.POST.get('circular_status'),
                    )
                    all_circular = circular_list.objects.values()
                    messages.success(request, 'Circular update successfully!')
                    return render(request, 'admin_dashboard/all_circulars.html',{ 'all_circular_info':all_circular})
                else:
                    circular_list.objects.filter(circular_id=request.POST.get('circular_id')).update(
                        circular_title=request.POST.get('circular_title'),
                        circular_date = request.POST.get('circular_date'), 
                        circular_status = request.POST.get('circular_status'),
                    )
                    all_circular = circular_list.objects.values()
                    messages.success(request, 'Circular update successfully!')
                    return render(request, 'admin_dashboard/all_circulars.html',{ 'all_circular_info':all_circular})
            
            update_circular = circular_list.objects.filter(circular_id = request.POST.get('circular_id')).values()
            param = {'update_data':update_circular,'username': request.session['user']}
            print(update_circular)
        return render(request, 'admin_dashboard/update_circular_info.html', param)
    return redirect('login')

def delete_circular(request):
    if 'user' in request.session:
        if request.method == 'POST':
            circular_file = circular_list.objects.filter(circular_id = request.POST.get('circular_id')).values_list('circular_file_name')
            print(circular_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Circulars/"+str(circular_file[0][0])))
            circular_list.objects.filter(circular_id = request.POST.get('circular_id')).delete()
            return redirect('all_circulars')
        return render(request, 'admin_dashboard/delete_circular.html', {'username': request.session['user']})

def all_tenders(request):
    if 'user' in request.session:
        all_tender = tender_list.objects.values()
        paginator = Paginator(all_tender, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_tenders.html',{ 'all_tenders_info':page_obj, 'username': request.session['user'] })
    return redirect('login')

def add_tender_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.FILES.get('tender_file_name'):
                fs = FileSystemStorage(location="application/static/uploads/Tenders")
                tender_file = request.FILES['tender_file_name']
                filename = fs.save(tender_file.name, tender_file)
                uploaded_tender_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                
                tender_data = tender_list(
                    tender_id = request.POST.get('tender_id'),
                    tender_title = request.POST.get('tender_title'),
                    tender_date = request.POST.get('tender_date'),
                    tender_file_name = uploaded_tender_file, 
                    tender_status = request.POST.get('tender_status')
                )
                tender_data.save()
                messages.success(request, 'tender added successfully!')
                return redirect('all_tenders')
            else:
                tender_data  =  tender_list(
                    tender_id = request.POST.get('tender_id'),
                    tender_title = request.POST.get('tender_title'),
                    tender_date = request.POST.get('tender_date'),
                    tender_status = request.POST.get('tender_status')
                )
                tender_data.save()
                messages.success(request, 'Tender added successfully!')
                return redirect('all_tenders')
        return render(request, 'admin_dashboard/add_tender_info.html', {'username': request.session['user']})
    return redirect('login')

def update_tender_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print("\n-----------------------------------")
                if request.FILES.get('tender_file_name'):
                    print("\n-----------------------------------")
                    fs = FileSystemStorage(location="application/static/uploads/Tenders")
                    tender_file = request.FILES['tender_file_name']
                    filename = fs.save(tender_file.name, tender_file)
                    uploaded_tender_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                    
                    
                    
                    tender_list.objects.filter(tender_id=request.POST.get('tender_id')).update(
                        tender_title=request.POST.get('tender_title'),
                        tender_date = request.POST.get('tender_date'),
                        tender_file_name = uploaded_tender_file, 
                        tender_status = request.POST.get('tender_status'),
                    )
                    all_tenders = tender_list.objects.values()
                    messages.success(request, 'Tender update successfully!')
                    return render(request, 'admin_dashboard/all_tenders.html',{ 'all_tenders_info':all_tenders})
                else:
                    tender_list.objects.filter(tender_id=request.POST.get('tender_id')).update(
                        tender_title=request.POST.get('tender_title'),
                        tender_date = request.POST.get('tender_date'), 
                        tender_status = request.POST.get('tender_status'),
                    )
                    all_tenders = tender_list.objects.values()
                    print(all_tenders)
                    messages.success(request, 'Tender update successfully!')
                    return render(request, 'admin_dashboard/all_tenders.html',{ 'all_tenders_info':all_tenders})
            
            update_tender = tender_list.objects.filter(tender_id = request.POST.get('tender_id')).values()
            param = {'update_data':update_tender,'username': request.session['user']}
            print(update_tender)
        return render(request, 'admin_dashboard/update_tender_info.html', param)
    return redirect('login')

def delete_tender(request):
    if 'user' in request.session:
        if request.method == 'POST':
            tender_file = tender_list.objects.filter(tender_id = request.POST.get('tender_id')).values_list('tender_file_name')
            print(tender_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Tenders/"+str(tender_file[0][0])))
            tender_list.objects.filter(tender_id = request.POST.get('tender_id')).delete()
            return redirect('all_tenders')
        return render(request, 'admin_dashboard/delete_tender.html', {'username': request.session['user']})
 
# Media Gallery
def all_media(request):
    if 'user' in request.session:
        all_media = media.objects.values()
        paginator = Paginator(all_media, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_dashboard/all_media.html',{ 'all_media_info':page_obj, 'username': request.session['user'] })
    return redirect('login')

def add_media_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.FILES.get('first_look_img'):
                if request.FILES.get('img'):
                    fs = FileSystemStorage(location="application/static/uploads/media")
                    first_look_img = request.FILES['first_look_img']
                    filename1 = fs.save(first_look_img.name, first_look_img)
                    uploaded_advertise_file = fs.url(filename1).replace('/media/', '').replace('% 20', ' ')
                    img = request.FILES['img']
                    filename2 = fs.save(img.name, img)
                    uploaded_advertise_file = fs.url(filename2).replace('/media/', '').replace('% 20', ' ')
                
                    media_data = media(
                        event_name = request.POST.get('event_name'),
                        img = filename2,
                        first_look_img = filename1,
                        media_status = request.POST.get('media_status'), 
                        event_details = request.POST.get('event_details'),
                    )
                    media_data.save()
                    messages.success(request, 'Advertise added successfully!')
                    return redirect('all_advertise')
            else:
                messages.warning(request, 'Don`t have Media file')
                return redirect('all_media')
        return render(request, 'admin_dashboard/add_media_info.html', {'username': request.session['user']})
    return redirect('login')

def update_media_info(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.POST.get('update_data') == 'update_data':
                print("\n-----------------------------------")
                if request.FILES.get('advertise_file_name'):
                    print("\n-----------------------------------")
                    fs = FileSystemStorage(location="application/static/uploads/Advertise")
                    advertise_file = request.FILES['advertise_file_name']
                    filename = fs.save(advertise_file.name, advertise_file)
                    uploaded_advertise_file = fs.url(filename).replace('/media/', '').replace('%20', ' ')
                    
                    
                    advertise_list.objects.filter(advertise_id=request.POST.get('advertise_id')).update(
                        advertise_title=request.POST.get('advertise_title'),
                        advertise_date = request.POST.get('advertise_date'),
                        advertise_file_name = uploaded_advertise_file, 
                        advertise_status = request.POST.get('advertise_status'),
                    )
                    all_advertise = advertise_list.objects.values()
                    messages.success(request, 'Advertise update successfully!')
                    return render(request, 'admin_dashboard/all_advertise.html',{ 'all_advertise_info':all_advertise})
                else:
                    advertise_list.objects.filter(advertise_id=request.POST.get('advertise_id')).update(
                        advertise_title=request.POST.get('advertise_title'),
                        advertise_date = request.POST.get('advertise_date'),
                        advertise_status = request.POST.get('advertise_status'),
                    )
                    all_advertise = advertise_list.objects.values()
                    messages.success(request, 'Advertise update successfully!')
                    return render(request, 'admin_dashboard/all_advertise.html',{ 'all_advertise_info':all_advertise})
            
            update_advertise = advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).values()
            param = {'update_data':update_advertise,'username': request.session['user']}
            print(update_advertise)
        return render(request, 'admin_dashboard/update_media_info.html', param)
    return redirect('login')

def delete_media(request):
    if 'user' in request.session:
        if request.method == 'POST':
            advertise_file = advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).values_list('advertise_file_name')
            print(advertise_file)
            os.remove(os.path.join(settings.MEDIA_ROOT,"../application/static/uploads/Advertise/"+str(advertise_file[0][0])))
            advertise_list.objects.filter(advertise_id = request.POST.get('advertise_id')).delete()
            return redirect('all_advertise')
        return redirect('all_media.html')
    