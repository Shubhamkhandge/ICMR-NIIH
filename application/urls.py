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
    path('scientists/', views.scientists, name='scientists'),
    path('scientist-details/', views.scientist_details, name='scientist-details'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)