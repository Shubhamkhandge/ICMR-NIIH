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
    path('departments/', views.departments, name='departments'),
    path('departments-details/', views.departments_details, name='departments-details'),
    
    # Staff-related pages
    path('scientist-staff/', views.scientist_staff, name='scientist-staff'),
    path('scientist-staff-details/', views.scientist_details, name='scientist-staff-details'),
    path('administration-staff/', views.admin_staff, name='administration-staff'),
    path('administration-staff-details/', views.administration_details, name='administration-staff-details'),
    path('technical-staff/', views.technical_staffs, name='technical-staff'),
    path('technical-staff-details/', views.technical_details, name='technical-staff-details'),
    path('project-staff/', views.project_staff_info, name='project-staff'),
    path('project-staff-details/', views.project_details, name='project-staff-details'),
    path('students-list/', views.students_list, name='students-list'),
    path('student-staff-details/', views.student_details, name='student-staff-details'),
    path('alumini-staff/', views.alumini_staff, name='alumini-staff'),
    path('alumini-staff-details/', views.alumini_details, name='alumini-staff-details'),
    
    # Publications and News
    path('publications-list/', views.publications, name='publications-list'),
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
    path('admin_dashboard/login', views.login_page, name='login'),
    path('admin_dashboard/logout', views.logout_page, name='logout'),

    # Dashboard URL
    path('admin_dashboard/dashboard', views.dashboard_view, name='dashboard'),

    # User-registration page
    path('admin_dashboard/admin_user_registration', views.admin_user_registration, name='admin_user_registration'),
    path('admin_dashboard/add_admin_user', views.add_admin_user, name='add_admin_user'),
    
    # About pages URL
    path('admin_dashboard/vision_info', views.vision_info, name='vision_info'),
    
    # Department Pages URL's
    path('admin_dashboard/all_departments', views.all_departments, name='all_departments'),
    path('admin_dashboard/add_department_info', views.add_department_info, name='add_department_info'),
    path('admin_dashboard/update_department_info', views.update_department_info, name='update_department_info'),
    path('admin_dashboard/delete_department', views.delete_department, name='delete_department'),
    
    # Support Department Pages URL's
    path('admin_dashboard/all_support_departments', views.all_support_departments, name='all_support_departments'),
    path('admin_dashboard/add_support_department_info', views.add_support_department_info, name='add_support_department_info'),
    path('admin_dashboard/update_support_department_info', views.update_support_department_info, name='update_support_department_info'),
    path('admin_dashboard/delete_support_department', views.delete_support_department, name='delete_support_department'),
    
    # Category URL's
    path('admin_dashboard/all_categories', views.all_categories, name='all_categories'),
    path('admin_dashboard/add_category_info', views.add_category_info, name='add_category_info'),
    path('admin_dashboard/update_category_info', views.update_category_info, name='update_category_info'),
    path('admin_dashboard/delete_category', views.delete_category, name='delete_category'),
    
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
    path('admin_dashboard/delete_admin', views.delete_admin, name='delete_admin'),
    
    # Technical Pages URL's
    path('admin_dashboard/all_technical_staff', views.all_technical_staff, name='all_technical_staff'),
    path('admin_dashboard/add_technical_info', views.add_technical_info, name='add_technical_info'),
    path('admin_dashboard/update_technical_info', views.update_technical_info, name='update_technical_info'),
    path('admin_dashboard/delete_technical', views.delete_technical, name='delete_technical'),
   
    # Project Pages URL's
    path('admin_dashboard/all_project_staff', views.all_project_staff, name='all_project_staff'),
    path('admin_dashboard/add_project_staff_info', views.add_project_staff_info, name='add_project_staff_info'),
    path('admin_dashboard/update_project_staff_info', views.update_project_staff_info, name='update_project_staff_info'),
    path('admin_dashboard/delete_project_staff', views.delete_project_staff, name='delete_project_staff'),
    
    # Project Pages URL's
    path('admin_dashboard/all_projects', views.all_projects, name='all_projects'),
    path('admin_dashboard/add_project_info', views.add_project_info, name='add_project_info'),
    path('admin_dashboard/update_project_info', views.update_project_info, name='update_project_info'),
    path('admin_dashboard/delete_project', views.delete_project, name='delete_project'),
    
    # Publications Pages URL's
    path('admin_dashboard/all_publications', views.all_publications, name='all_publications'),
    path('admin_dashboard/add_publication_info', views.add_publication_info, name='add_publication_info'),
    path('admin_dashboard/update_publication_info', views.update_publication_info, name='update_publication_info'),
    path('admin_dashboard/delete_publication', views.delete_publication, name='delete_publication'),
    
    # Bulletins Pages URL's
    path('admin_dashboard/all_niih_bulletins', views.all_niih_bulletins, name='all_niih_bulletins'),
    path('admin_dashboard/add_niih_bulletin_info', views.add_niih_bulletin_info, name='add_niih_bulletin_info'),
    path('admin_dashboard/update_niih_bulletin_info', views.update_niih_bulletin_info, name='update_niih_bulletin_info'),
    path('admin_dashboard/delete_niih_bulletin', views.delete_niih_bulletin, name='delete_niih_bulletin'),
    
    # Newsletters Pages URL's
    path('admin_dashboard/all_newsletters', views.all_newsletters, name='all_newsletters'),
    path('admin_dashboard/add_newsletter_info', views.add_newsletter_info, name='add_newsletter_info'),
    path('admin_dashboard/update_newsletter_info', views.update_newsletter_info, name='update_newsletter_info'),
    path('admin_dashboard/delete_newsletter', views.delete_newsletter, name='delete_newsletter'),
    
    # Awards Pages URL's
    path('admin_dashboard/all_awards', views.all_awards, name='all_awards'),
    path('admin_dashboard/add_award_info', views.add_award_info, name='add_award_info'),
    path('admin_dashboard/update_award_info', views.update_award_info, name='update_award_info'),
    path('admin_dashboard/delete_award', views.delete_award, name='delete_award'),
    
    # Settings Page URL
    path('admin_dashboard/settings', views.settings_page, name='settings'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)