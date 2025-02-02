from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("admin_profile/", views.admin_profile, name="admin-dashboard-profile"),
    path("create/admin/", views.create_admin, name="admin-create-new"),

    path("admin_masterlist/", views.admin_masterlist, name="admin-dashboard-masterlist"),
    path("admin_enrollment/", views.admin_enrollment, name="admin-dashboard-enrollment"),
    
    path("admin_checklist/", views.admin_checklist, name="admin-dashboard-checklist"),
    path("admin_checklist/<str:student_number>/", views.admin_checklist, name="admin-dashboard-checklist"),
    path("add_grades/", views.grades_input, name="grades_input"),
    path("add_grades/<str:student_number>", views.grades_input, name="grades_input"),
    path("grades/input/<str:student_number>/", views.grades_input_view, name="grades_input_view"),

    path("print_cor/", views.print_cor, name='print_cor'),
    path("edit_info/<str:student_number>", views.edit_info, name='edit_info'),
    path("process_cor/<str:student_number>", views.process_cor, name='process_cor'),
    path("update_info/<str:student_number>", views.update_info, name='update_info'),
    path("print_cor/<str:student_number>", views.print_cor, name='print_cor'),

    path("enroll_student/<str:enrollee_type>/", views.enroll_student, name='enroll_student'),
    path("search_students/", views.search_students, name='search_students'),
    
    path("configure/", views.admin_config, name="admin_config"),
    path('save_subject/', views.save_subject, name='save_subject'),
    path("delete_subject/<str:subject_id>/", views.delete_subject, name='delete_subject'),
    path('save_instructor/', views.save_instructor, name='save_instructor'),
    path("delete_instructor/<str:instructor_id>/", views.delete_instructor, name='delete_instructor'),

    path("admin_adjust_fees/", views.adjust_fees, name="adjust_fees"),
    path("admin_set_fees/", views.set_fees, name="set_fees"),
    path("set_enrollment_date_view/", views.set_enrollment_date_view, name="set_enrollment_date_view"),
    path("set_enrollment_date/", views.set_enrollment_date, name="set_enrollment_date"),
]
