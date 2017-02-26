from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^faculty/', views.faculty, name="faculty"),
    url(r'^student/', views.student, name="student"),
    url(r'^homefaculty/', views.homefaculty, name="homefaculty"),
    url(r'^homestudent/', views.homestudent, name="homestudent"),
    url(r'^faculty1/', views.faculty1, name="faculty1"),
]
