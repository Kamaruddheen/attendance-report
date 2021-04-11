from django.shortcuts import render
from django.http import JsonResponse

from attendancess.models import *
from user_module.models import *
from classroom.models import *


def dashboard_view(request):
    data = []
    Present_count = 0
    Absent_count = 0

    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(status="Present").count()
    Absent_count = AttendanceModel.objects.filter(status="Absent").count()

    total = float(Present_count) + float(Absent_count)
    Present_per = "{:.2f}".format((Present_count / total) * 100)
    Absent_per = "{:.2f}".format((Absent_count / total) * 100)

    # passing presentage data for doughnut chart
    data = [Present_per, Absent_per]

    # Total number of students
    total_stud_count = AttendanceModel.objects.values(
        'rollno').distinct().count()
    staff_count = User.objects.filter(user_type=2).count()

    context = {
        'data': data,
        'total': total_stud_count,
        'staff': staff_count,
        'present': Present_count,
        'absent': Absent_count,
    }
    return render(request, "dashboard/dashboard.html", context=context)


def attendance_classwise(request):
    classes = []
    present = []
    absent = []

    list_of_classrooms = AttendanceIdModel.objects.values(
        'classroom').distinct()
    print(list_of_classrooms)
    for clas in list_of_classrooms:
        cla = ClassroomModel.objects.filter(id=clas['classroom'])
        for c in cla:
            classes.append(str(c).upper())
        class_present = AttendanceModel.objects.filter(
            attendance_id__classroom=clas['classroom'], status="Present").count()
        class_absent = AttendanceModel.objects.filter(
            attendance_id__classroom=clas['classroom'], status="Absent").count()
        present.append(class_present)
        absent.append(class_absent)

    print(classes)
    print(present, absent)

    return JsonResponse({
        'labels': classes,
        'present': present,
        'absent': absent,
    })


# Particular student data
def student_details(request):
    rollno = request.POST.get('rollno', None)
    # print(rollno)
    data = AttendanceModel.objects.filter(
        rollno=rollno).order_by('attendance_id')
    details = {
        'data': data
    }
    return render(request, "dashboard/dashboard.html", details)
