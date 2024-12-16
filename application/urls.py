from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('vision-mission-mandate/', views.vision_mission_mandate, name='vision-mission-mandate'),
    path('organogram/', views.organogram, name='organogram'),
    path('niih-leadership/', views.niih_leadership, name='niih-leadership'),
    path('our-director/', views.our_director, name='our-director'),
    path('departments/', views.departments, name='departments'),
    path('departments-details/', views.departments_details, name='departments-details'),
    path('awards-achievements/', views.awards_achievements, name='awards-achievements'),
    path('former-directors/', views.former_directors, name='former-directors'),
    path('contact-directory/', views.contact_directory, name='contact-directory'),
    path('scientist-staff/', views.scientist_staff, name='scientist-staff'),
    path('scientist-details/', views.scientist_details, name='scientist-details'),
    path('administration-staff/', views.administration_staff, name='administration-staff'),
    path('administration-details/', views.administration_details, name='administration-details'),
    path('technical-staff/', views.technical_staff, name='technical-staff'),
    path('technical-details/', views.technical_details, name='technical-details'),
    path('project-staff/', views.project_staff, name='project-staff'),
    path('project-details/', views.project_details, name='project-details'),
    path('students-list/', views.students_list, name='students-list'),
    path('student-details/', views.student_details, name='student-details'),
    path('alumini-staff/', views.alumini_staff, name='alumini-staff'),
    path('alumini-details/', views.alumini_details, name='alumini-details'),
    path('publications-list/', views.publications_list, name='publications-list'),
    path('niih-bulletin-list/', views.niih_bulletin_list, name='niih-bulletin-list'),
    path('bgrc-news-letter/', views.bgrc_news_letter, name='bgrc-news-letter'),
    path('ongoing-projects-list/', views.ongoing_projects_list, name='ongoing-projects-list'),
    path('completed-projects-list/', views.completed_projects_list, name='completed-projects-list'),
    path('media-gallery/', views.media_gallery, name='media-gallery'),
    path('circulars-list/', views.circulars_list, name='circulars-list'),
    path('reports-list/', views.reports_list, name='reports-list'),
    path('tenders-list/', views.tenders_list, name='tenders-list'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)