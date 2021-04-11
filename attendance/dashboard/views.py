from django.shortcuts import render
from django.http import JsonResponse

from attendancess.models import *
from user_module.models import *
from classroom.models import *


def dashboard_view(request):
    classes = []

    # collecting class list
    list_of_classrooms = AttendanceIdModel.objects.values(
        'classroom').distinct()

    for clas in list_of_classrooms:
        cla = ClassroomModel.objects.filter(id=clas['classroom'])
        for c in cla:
            # storing name of class
            classes.append(c)

    context = {
        'classes': classes
    }
    return render(request, "dashboard/dashboard.html", context=context)


# Class-wise Attendance stacked-bar chart
def attendance_classwise(request):
    classes = []
    present = []
    absent = []

    # collecting class list
    list_of_classrooms = AttendanceIdModel.objects.values(
        'classroom').distinct()

    for clas in list_of_classrooms:
        cla = ClassroomModel.objects.filter(id=clas['classroom'])
        for c in cla:
            # storing name of class
            classes.append(str(c).upper())
        class_present = AttendanceModel.objects.filter(
            attendance_id__classroom=clas['classroom'], status="Present").count()
        class_absent = AttendanceModel.objects.filter(
            attendance_id__classroom=clas['classroom'], status="Absent").count()
        # storing total present of particular class
        present.append(class_present)
        # storing total absent of particular class
        absent.append(class_absent)

    return JsonResponse({
        'labels': classes,
        'present': present,
        'absent': absent,
    })


# Overall Percentage
def over_per():
    overall_percentage = []
    Present_count = 0
    Absent_count = 0

    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(status="Present").count()
    Absent_count = AttendanceModel.objects.filter(status="Absent").count()

    total = float(Present_count) + float(Absent_count)
    Present_per = "{:.2f}".format((Present_count / total) * 100)
    Absent_per = "{:.2f}".format((Absent_count / total) * 100)

    # passing presentage data for doughnut chart
    overall_percentage = [Present_per, Absent_per]

    return overall_percentage


# Overall Totals
def over_tot():
    # Total number of students
    total_stud_count = AttendanceModel.objects.values(
        'rollno').distinct().count()
    # Total number of staff
    staff_count = User.objects.filter(user_type=2).count()
    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(status="Present").count()
    Absent_count = AttendanceModel.objects.filter(status="Absent").count()

    return total_stud_count, staff_count, Present_count, Absent_count


# Class-wise all type of data
def all_data(request):
    # * Default
    # Percentage of All Data
    overall_percentage = over_per()
    # Student, Staff, Present, Absent
    total_stud_count, staff_count, Present_count, Absent_count = over_tot()

    return JsonResponse({
        'total': total_stud_count,
        'staff': staff_count,
        'present': Present_count,
        'absent': Absent_count,
        'overall_perc': overall_percentage
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
