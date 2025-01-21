from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.student_home, name="student-home"), 
    path("profile/", views.student_profile, name="student-profile"),
    path("checklist/", views.student_checklist, name="student-checklist"),
]
