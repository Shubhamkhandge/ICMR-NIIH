from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home and basic pages
    path('', views.home, name="home"),
    path('vision-mission-mandate/', views.vision_mission_mandate, name='vision-mission-mandate'),
    path('organogram/', views.organogram, name='organogram'),
    path('niih-leadership/', views.niih_leadership, name='niih-leadership'),
    path('our-director/', views.our_director, name='our-director'),
    path('former-directors/', views.former_directors, name='former-directors'),
    path('awards-achievements/', views.awards_achievements, name='awards-achievements'),
    path('contact-directory/', views.contact_directory, name='contact-directory'),
    
    # Department-related pages
    path('departments/', views.departments_list, name='departments'),
    path('departments-details/', views.departments_details, name='departments-details'),
    
    # Staff-related pages
    path('scientist-staff/', views.scientist_staff, name='scientist-staff'),
    path('scientist-staff-details/', views.scientist_details, name='scientist-staff-details'),
    path('administration-staff/', views.administration_staff, name='administration-staff'),
    path('administration-staff-details/', views.administration_details, name='administration-staff-details'),
    path('technical-staff/', views.technical_staff, name='technical-staff'),
    path('technical-staff-details/', views.technical_details, name='technical-staff-details'),
    path('project-staff/', views.project_staff, name='project-staff'),
    path('project-staff-details/', views.project_details, name='project-staff-details'),
    path('students-list/', views.students_list, name='students-list'),
    path('student-staff-details/', views.student_details, name='student-staff-details'),
    path('alumini-staff/', views.alumini_staff, name='alumini-staff'),
    path('alumini-staff-details/', views.alumini_details, name='alumini-staff-details'),
    
    # Publications and News
    path('publications-list/', views.publications_list, name='publications-list'),
    path('niih-bulletin-list/', views.niih_bulletin_list, name='niih-bulletin-list'),
    path('bgrc-news-letter/', views.bgrc_news_letter, name='bgrc-news-letter'),
    
    # Projects
    path('ongoing-projects-list/', views.ongoing_projects_list, name='ongoing-projects-list'),
    path('completed-projects-list/', views.completed_projects_list, name='completed-projects-list'),
    
    # Media and Photo Details
    path('media-gallery/', views.media_gallery, name='media-gallery'),
    path('photo-details/', views.photo_details, name='photo-details'),
    
    # Reports and Cirulars, Tenders
    path('circulars-list/', views.circulars_list, name='circulars-list'),
    path('advertise-list/', views.advertise_list, name='advertise-list'),
    path('reports-list/', views.reports_list, name='reports-list'),
    path('tenders-list/', views.tenders_list, name='tenders-list'),
    
    # Dashboard URL's
    # Login Authentication and Logout
    path('', views.login_page, name='login'),
    path('admin_dashboard/login', views.login_page, name='login'),
    # path('dashboard/logout', views.logout_page, name='logout'),

    # Dashboard URL
    path('admin_dashboard/dashboard', views.dashboard_view, name='dashboard'),
    # User-registration page
    path('admin_dashboard/user_registration', views.user_registration, name='user_registration'),
    # About pages URL
    path('admin_dashboard/vision_info', views.vision_info, name='vision_info'),
    # Department Pages URL's
    path('admin_dashboard/all_departments', views.all_departments, name='all_departments'),
    path('admin_dashboard/add_department_info', views.add_department_info, name='add_department_info'),
    path('admin_dashboard/update_department_info', views.update_department_info, name='update_department_info'),
    # Support Department URL's
    path('admin_dashboard/all_support_departments', views.all_support_departments, name='all_support_departments'),
    path('admin_dashboard/add_support_department_info', views.add_support_department_info, name='add_support_department_info'),
    path('admin_dashboard/update_support_department_info', views.update_support_department_info, name='update_support_department_info'),
    path('admin_dashboard/delete_support_department', views.delete_support_department, name='delete_support_department'),
    # Designation Pages URL's
    path('admin_dashboard/all_designations', views.all_designations, name='all_designations'),
    path('admin_dashboard/add_designation_info', views.add_designation_info, name='add_designation_info'),
    path('admin_dashboard/update_designation_info', views.update_designation_info, name='update_designation_info'),
    path('admin_dashboard/delete_designation_info', views.delete_designation_info, name='delete_designation_info'),
    # Staff URL's
    # Scientist Pages URL's
    path('admin_dashboard/all_scientists_staff', views.all_scientists_staff, name='all_scientists_staff'),
    path('admin_dashboard/add_scientist_info', views.add_scientist_info, name='add_scientist_info'),
    path('admin_dashboard/update_scientist_info', views.update_scientist_info, name='update_scientist_info'),
    path('admin_dashboard/delete_scientist', views.delete_scientist, name='delete_scientist'),
    # Administration Pages URL's
    path('admin_dashboard/all_admin_staff', views.all_admin_staff, name='all_admin_staff'),
    path('admin_dashboard/add_admin_info', views.add_admin_info, name='add_admin_info'),
    path('admin_dashboard/update_admin_info', views.update_admin_info, name='update_admin_info'),
    # Project Pages URL's
    path('admin_dashboard/all_projects', views.all_projects, name='all_projects'),
    path('admin_dashboard/add_project_info', views.add_project_info, name='add_project_info'),

    # Settings Page URL
    path('admin_dashboard/settings', views.settings_page, name='settings'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)