from django.shortcuts import render
from django.http import JsonResponse

from attendancess.models import AttendanceIdModel, AttendanceModel
from user_module.models import User
from classroom.models import ClassroomModel
from subject.models import HourModel, SubjectModel


# Dashboard html render area
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
    Present_count, Absent_count, Present_per, Absent_per = 0, 0, 0, 0

    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(status="Present").count()
    Absent_count = AttendanceModel.objects.filter(status="Absent").count()

    total = float(Present_count) + float(Absent_count)
    if not total == 0:
        Present_per = "{:.2f}".format((Present_count / total) * 100)
        Absent_per = "{:.2f}".format((Absent_count / total) * 100)
    else:
        # error message
        pass

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


# Particular Class Present & Absent Percentage
def class_per(att_obj):
    overall_percentage = []
    Present_count, Absent_count, Present_per, Absent_per = 0, 0, 0, 0

    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(
        status="Present", attendance_id__in=att_obj).count()
    Absent_count = AttendanceModel.objects.filter(
        status="Absent", attendance_id__in=att_obj).count()

    total = float(Present_count) + float(Absent_count)
    if not total == 0:
        Present_per = "{:.2f}".format((Present_count / total) * 100)
        Absent_per = "{:.2f}".format((Absent_count / total) * 100)
    else:
        # error message
        pass

    # passing presentage data for doughnut chart
    overall_percentage = [Present_per, Absent_per]

    return overall_percentage


# Particular Class Totals
def class_tot(att_obj, classroom_id):
    # Total number of students
    total_stud_count = AttendanceModel.objects.filter(attendance_id__in=att_obj).values(
        'rollno').distinct().count()
    # Total number of staff
    hours = HourModel.objects.filter(classroom=classroom_id)
    subjects = []
    for hour in hours:
        subjects.append(hour)
    staff_count = SubjectModel.objects.filter(
        hour__in=tuple(subjects)).count()
    # Total Present & Absent Status
    Present_count = AttendanceModel.objects.filter(
        attendance_id__in=att_obj, status="Present").count()
    Absent_count = AttendanceModel.objects.filter(
        status="Absent", attendance_id__in=att_obj).count()

    return total_stud_count, staff_count, Present_count, Absent_count


# Class-wise all type of data
def all_data(request):
    # * Default
    # Percentage of All Data
    overall_percentage = over_per()
    # Student, Staff, Present, Absent
    total_stud_count, staff_count, Present_count, Absent_count = over_tot()

    if request.method == "POST":
        classroom_id = request.POST.get('class_id', None)
        Attendance_id_obj = AttendanceIdModel.objects.filter(
            classroom__id=classroom_id)
        attend_id = []
        for attendance in Attendance_id_obj:
            attend_id.append(attendance.id)

        # Particular classroom Totals & OverAll
        overall_percentage = class_per(tuple(attend_id))
        total_stud_count, staff_count, Present_count, Absent_count = class_tot(
            tuple(attend_id), classroom_id)

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
