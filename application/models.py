from django.db import models
from django.contrib.auth.models import User

# Model to track logged-in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete = models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
# Model for advertise
class advertise(models.Model):
    advertise_title = models.CharField(max_length=255, null=True)
    advertise_file_name = models.CharField(max_length=255, null=True)
    Show_1 = models.TextField()
    date_sub = models.DateTimeField(null=True)

# Model for alumini staff
class alumini(models.Model):
    alumini_name = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    year_leaving = models.CharField(max_length=255, null=True)

# Model for appointment
class appointment(models.Model):
    patient_name = models.CharField(max_length=255, null=True)
    departmemt_name = models.CharField(max_length=255, null=True)
    doctor_name = models.CharField(max_length=255, null=True)
    doctor_email = models.EmailField(max_length=100, null=True)
    hospital_name = models.CharField(max_length=255, null=True)
    patient_age = models.CharField(max_length=255, null=True)
    patient_dob = models.DateField(null=True)
    patient_relationship = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    patient_father_name = models.CharField(max_length=255, null=True)
    patient_mother_name = models.CharField(max_length=255, null=True)
    patient_address = models.TextField()
    phone_no = models.CharField(max_length=255, null=True)
    patient_email = models.EmailField(max_length=100, null=True)
    date_time = models.DateTimeField(null=True)
    birth_weight = models.CharField(max_length=255, null=True)
    referring_doctor = models.CharField(max_length=255, null=True)
    contact_no_doctor = models.CharField(max_length=255, null=True)
    # doctor_email_id = models.CharField(max_length=255, null=True)
    presenting_complaints = models.TextField()
    any_queries = models.TextField()
    report_file = models.CharField(max_length=255, null=True)

# Model for award
class award(models.Model):
    award_name = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=255, null=True)

# Model for bgrc_news
class bgrc_news(models.Model):
    bgrc_news_name = models.CharField(max_length=255, null=True)
    vol_no = models.CharField(max_length=255, null=True)
    bgrc_news_month = models.CharField(max_length=255, null=True)
    bgrc_news_year = models.CharField(max_length=255, null=True)
    data_created = models.DateTimeField(null=True)

# Model for bulletin
class bulletin(models.Model):
    bulletin_name = models.CharField(max_length=255, null=True)
    vol_no = models.CharField(max_length=255, null=True)
    bulletin_month = models.CharField(max_length=255, null=True)
    bulletin_year = models.CharField(max_length=255, null=True)
    bulletin_file_name = models.CharField(max_length=300, null=True)
    data_created = models.DateTimeField(null=True)

class committee(models.Model):
    library_type = models.CharField(max_length=255, null=True)
    about_committee = models.TextField()
    image_name = models.CharField(max_length=255, null=True)

class cv_photo(models.Model):
    photo_title = models.TextField(max_length=255, null=True)
    photo_f = models.CharField(max_length=255, null=True)
    Show_1 = models.CharField(max_length=255, null=True)
    date_sub = models.DateTimeField(null=True)

# Model for Department (single entry)
class department(models.Model):
    department_id = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)  # Changed field name to avoid conflict
    hod_id = models.CharField(max_length=255, null=True)
    hod_name = models.CharField(max_length=255, null=True)
    department_info = models.CharField(max_length=255, null=True)

# Model for Departments (list of departments)
class departments(models.Model):
    department_id = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)  # Renamed to avoid conflict
    hod = models.CharField(max_length=255, null=True)
    about_department1 = models.TextField(null=True)
    about_department2 = models.TextField(null=True)
    about_department3 = models.TextField(null=True)
    about_research = models.TextField(null=True)
    research_projects = models.TextField(null=True)
    display_order = models.CharField(max_length=255, null=True)
    data_created = models.DateTimeField(auto_now_add=True, null=False)  # Ensured null=False for clarity

class departments_test(models.Model):
    department_id = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    test_name = models.CharField(max_length=255, null=True)

class niih_projects(models.Model):
    project_id = models.CharField(max_length=255, null=True)  # Nullable but blank allowed
    project_name = models.CharField(max_length=200, null=True)
    project_incharge = models.CharField(max_length=255, null=True)
    scientist_id = models.CharField(max_length=255, null=True)
    fa = models.CharField(max_length=255, null=True)
    di = models.CharField(max_length=255, null=True)
    dc = models.CharField(max_length=255, null=True)
    tf = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Corrected DecimalField
    project_year = models.IntegerField(blank=True, null=True)  # Changed to IntegerField
    on_going = models.CharField(max_length=255, null=True)
    department_id = models.CharField(max_length=255, null=True)
    project_proposal = models.CharField(max_length=255, null=True)  # Fixed typo ('praposal' to 'proposal')
    project_status = models.CharField(max_length=255, null=True)
    project_result = models.CharField(max_length=255, null=True)
    project_budget = models.CharField(max_length=100, null=True)  # Changed to blank=True, null=True is not necessary

class icc_women(models.Model):
    Complainant_name = models.CharField(max_length=255, null=True)
    Complainant_Designation = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    contact_no = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    Name_of_Accused = models.CharField(max_length=255, null=True)
    Designation_of_Accused = models.CharField(max_length=255, null=True)
    Working_Relationship = models.CharField(max_length=255, null=True)
    registered_with_ICC = models.CharField(max_length=255, null=True)
    complaint = models.TextField()
    chk1 = models.CharField(max_length=255, null=True)
    chk2 = models.CharField(max_length=255, null=True)
    chk3 = models.CharField(max_length=255, null=True)
    date_sub = models.DateTimeField(null=True)
    
class instrument(models.Model):
    instrument_id = models.CharField(max_length=255, null=True)
    instrument_name = models.CharField(max_length=255, null=True)
    instrument_description = models.TextField(null=True)
    image_name = models.CharField(max_length=255, null=True)
    data_created = models.DateTimeField(null=True)  # Changed to DateTimeField

class library(models.Model):
    library_type = models.CharField(max_length=255, null=True)
    type_description = models.TextField()
    image_name = models.CharField(max_length=255, null=True)

class niih_publications(models.Model):
    publication_title = models.CharField(max_length=255, null=True)
    author_name = models.CharField(max_length=255, null=True)
    journal_name = models.CharField(max_length=255, null=True)
    publication_year = models.CharField(max_length=255, null=True)
    publication_month = models.CharField(max_length=255, null=True)
    journal_type = models.CharField(max_length=255, null=True)
    user_id = models.CharField(max_length=255, null=True)

class niih_staff(models.Model):
    staff_id = models.CharField(max_length=255, null=True)
    staff_name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    author_name = models.CharField(max_length=255, null=True)
    hod_id = models.CharField(max_length=255, null=True)
    category_name = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    department_id = models.CharField(max_length=255, null=True)
    staff_email = models.CharField(max_length=255, null=True)
    phone_no = models.CharField(max_length=255, null=True)
    addhar_no = models.CharField(max_length=255, null=True)
    image_name = models.CharField(max_length=255, null=True)
    name_guide = models.CharField(max_length=255, null=True)
    year_join = models.CharField(max_length=255, null=True)
    staff_qualifications = models.CharField(max_length=255, null=True)
    staff_specialization = models.CharField(max_length=255, null=True)
    date_cp = models.CharField(max_length=255, null=True)
    level_no = models.CharField(max_length=255, null=True)

class department_staff(models.Model):
    department_id = models.CharField(max_length=255, null=True)
    hod_name = models.CharField(max_length=255, null=True)  # Renamed to avoid conflict
    designation = models.CharField(max_length=255, null=True)
    email_id = models.EmailField(max_length=255, null=True)
    display_order = models.CharField(max_length=255, null=True)
    data_created = models.DateTimeField(null=True)  # Changed to DateTimeField

# Model for Scientific Staff
class scientific_staff(models.Model):
    staff_name = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    email_id = models.EmailField(max_length=200, null=True)
    image_name = models.CharField(max_length=255, null=True)
    phone_no = models.CharField(max_length=255, null=True)
    fax_no = models.CharField(max_length=255, null=True)
    academic_background = models.TextField()
    professional_experience = models.TextField()
    research_interests = models.TextField()
    awards_achievements = models.TextField()
    publications = models.TextField()
    projects = models.TextField()
    research_staff = models.CharField(max_length=255, null=True)
    display_order = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=True)  # Changed to BooleanField
    data_created = models.DateTimeField(null=True)  # Changed to DateTimeField

# Model for Scientific Staff
class admin_staff(models.Model):
    staff_name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255,null=True)

class out_publications(models.Model):
    publication_title = models.CharField(max_length=255, null=True)
    author_name = models.CharField(max_length=255, null=True)
    journal_name = models.CharField(max_length=255, null=True)
    publication_type = models.CharField(max_length=255, null=True)
    publication_month = models.CharField(max_length=255, null=True)
    publication_month_number = models.CharField(max_length=255, null=True)
    publication_year = models.CharField(max_length=255, null=True)
    staff_id = models.CharField(max_length=255, null=True)
    select_publication = models.CharField(max_length=255, null=True)

class project_new(models.Model):
    project_incharge = models.CharField(max_length=255, null=True)
    project_title = models.CharField(max_length=255, null=True)
    scientist_id = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    on_going = models.CharField(max_length=255, null=True)

class publication_copy(models.Model):
    publication_title = models.CharField(max_length=255, null=True)
    author_name = models.CharField(max_length=255, null=True)
    journal_name = models.CharField(max_length=255, null=True)
    publication_type = models.CharField(max_length=255, null=True)
    publication_month = models.CharField(max_length=255, null=True)
    publication_month_number = models.CharField(max_length=255, null=True)
    publication_year = models.CharField(max_length=255, null=True)
    staff_id = models.CharField(max_length=255, null=True)
    select_publication = models.CharField(max_length=255, null=True)

class staff_new(models.Model):
    staff_name = models.CharField(max_length=255, null=True)
    guide_name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    department_name = models.CharField(max_length=255, null=True)
    category_name = models.CharField(max_length=255, null=True)
    join_year = models.CharField(max_length=255, null=True)

class login_data(models.Model):
    user_name = models.CharField(max_length=255, null=True)
    login_date = models.CharField(max_length=255, null=True)
    login_time = models.CharField(max_length=255, null=True)
    success_attempt = models.CharField(max_length=255, null=True)
    failure_attempt = models.CharField(max_length=255, null=True)
    ipaddr = models.CharField(max_length=255, null=True)

class user(models.Model):
    full_name = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=255, null=True)
    user_password = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    staff_id = models.CharField(max_length=255, null=True)
    category_name = models.CharField(max_length=255, null=True)
    catcategory_work = models.CharField(max_length=255, null=True)
    level_no = models.CharField(max_length=255, null=True)

class admin_user(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)