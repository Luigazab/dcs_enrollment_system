from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import student, ChecklistItem, Subject
from django.db.models import Q

@login_required
def student_home(request):
    try:
        student_profile = student.objects.get(user=request.user)
    except student.DoesNotExist:
        student_profile = None

    return render(request, "student_dashboard/index.html", {'student': student_profile})

@login_required
def student_profile(request):
    try:
        student_profile = student.objects.get(user=request.user)
    except student.DoesNotExist:
        student_profile = None
    return render(request, "student_dashboard/profile.html",{'student': student_profile})

def student_status(request):

    return render(request, "student_dashboard/status.html",{})

def student_cor(request):
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
            Q(course_title__icontains=search_query))
    else:
        # Default query with no search
        enrolled_items = checklist_items.all()
    
    year_semester_subjects ={}
    for year in range(1, 5):
        for sem in [1, 2]:
            subjects = all_subjects.filter(year=year, semester=sem)
            enrolled = checklist_items.filter(subject__in=subjects)

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
