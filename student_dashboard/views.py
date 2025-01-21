from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import student, ChecklistItem, Subject, Checklist
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def student_home(request):
    try:
        student_profile = student.objects.get(user=request.user)
        checklist = Checklist.objects.get(student=request.user)
        pending_subjects = checklist.items.filter(status="Pending") 
        passed_subjects_count = checklist.items.filter(status="Passed").count()
        pending_subjects_count = pending_subjects.count()
    except student.DoesNotExist:
        student_profile = None
        pending_subjects = None
        pending_subjects_count = 0
        passed_subjects_count = 0

    return render(request, "student_dashboard/index.html", {'student': student_profile,'pending_subjects': pending_subjects,'pending_subjects_count': pending_subjects_count,'passed_subjects_count': passed_subjects_count,})

@login_required
def student_profile(request):
    try:
        student_profile = student.objects.get(user=request.user)
    except student.DoesNotExist:
        student_profile = None
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        if new_password and confirm_new_password:
            if new_password == confirm_new_password:
                # Update the user's password
                user = request.user
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect("student-profile")  # Redirect to login for re-authentication
            else:
                messages.error(request, "Passwords do not match. Please try again.")
        else:
            messages.error(request, "Both password fields are required.")
    return render(request, "student_dashboard/profile.html",{'student': student_profile})

def student_checklist(request):
    student_display = get_object_or_404(student, user=request.user)
    checklist_items =ChecklistItem.objects.filter(checklist__student=student_display.user)
    all_subjects = Subject.objects.filter(program=student_display.course)

    search_query = request.POST.get("search_query", "").strip()
    if search_query:
        # Filter checklist and subjects using the search query
        enrolled_items = checklist_items.filter(
            Q(subject__course_code__icontains=search_query) |
            Q(subject__course_title__icontains=search_query) |
            Q(grade__icontains=search_query) |
            Q(instructor__name__icontains=search_query) |
            Q(status__icontains=search_query)
        )
        # Limit subjects to those found in search results
        all_subjects = Subject.objects.filter(Q(course_code__icontains=search_query) |
            Q(course_title__icontains=search_query), program=student_display.course)
    else:
        # Default query with no search
        enrolled_items = checklist_items.all()
    
    year_semester_subjects ={}
    for year in range(1, 5):
        for sem in [1, 2]:
            subjects = all_subjects.filter(year=year, semester=sem)
            enrolled = enrolled_items.filter(subject__in=subjects)

            enrolled_dict = {item.subject: item for item in enrolled}

            year_semester_subjects[f"Year {year} - Semester {sem}"] = [
                {"subject": subj, "status": "Not Enrolled"} if subj not in enrolled_dict
                else {"subject": subj, "status": enrolled_dict[subj].status, "grade": enrolled_dict[subj].grade, "instructor": enrolled_dict[subj].instructor}
                for subj in subjects
            ]
    for key in year_semester_subjects:
        if not year_semester_subjects[key]:
            year_semester_subjects[key] = [{
                "subject": None,
                "status": "No subjects match for this semester",
                "grade": None,
                "instructor": None,
            }]
    return render(request, "student_dashboard/checklist.html",{"student": student_display, "year_semester_subjects": year_semester_subjects,"search_query":search_query,})
