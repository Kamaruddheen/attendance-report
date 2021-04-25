from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta, date

from attendancess.models import AttendanceIdModel, AttendanceModel
from user_module.models import User
from classroom.models import ClassroomModel
from subject.models import HourModel, SubjectModel


# Dashboard html render area
def dashboard_view(request):
    classes = []

    # collecting class list in order of classroom by year then classroom of sec
    list_of_classrooms = AttendanceIdModel.objects.order_by('classroom__year', 'classroom__sec').values(
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

    # collecting class list in order of classroom by year then classroom of sec
    list_of_classrooms = AttendanceIdModel.objects.order_by('classroom__year', 'classroom__sec').values(
        'classroom').distinct()

    for clas in list_of_classrooms:
        cla = ClassroomModel.objects.filter(id=clas['classroom'])
        for c in cla:
            # storing name of class
            classes.append(str(c.get_year_display()).upper() +
                           " " + str(c.sec).upper())
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


# finding the last day of month from given_date year (month)
def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - timedelta(days=next_month.day)


# Class-wise Attendance stacked-bar chart (date)
def all_day_calender(request):
    # Date wise + getting the date from user
    dates = []
    present = []
    absent = []
    given_date = request.POST.get('current_date', date.today())

    # collecting previous date list-
    sdate = datetime.strptime(
        str(given_date), "%Y-%m-%d").date() - timedelta(days=4)
    edate = datetime.strptime(
        str(given_date), "%Y-%m-%d").date() + timedelta(days=3)

    list_of_dates = [
        sdate+timedelta(days=x) for x in range((edate-sdate).days) if datetime.strptime(str(sdate+timedelta(days=x)), "%Y-%m-%d").date().strftime("%A") != "Sunday"
    ]

    # Fetching attendance Present & Absent count
    for date1 in list_of_dates:
        class_present = AttendanceModel.objects.filter(
            attendance_id__date=date1, status="Present").count()
        class_absent = AttendanceModel.objects.filter(
            attendance_id__date=date1, status="Absent").count()
        dates.append(date1.day)
        # storing total present of particular class
        present.append(class_present)
        # storing total absent of particular class
        absent.append(class_absent)

    return JsonResponse({
        'labels': dates,
        'present': present,
        'absent': absent,
    })


# Class-wise Attendance stacked-bar chart (week)
def all_week_calender(request):
    dates = []
    present = []
    absent = []
    list_of_dates = []
    given_date = request.POST.get('current_date', date.today())

    # change str of date to date type
    dt = datetime.strptime(str(given_date), '%Y-%m-%d').date()
    # first and last date of the month
    initial_day_of_month = dt.replace(day=1)
    next_month = (dt.replace(day=28) + timedelta(days=4))
    last_day_of_month = next_month - timedelta(days=next_month.day)

    while last_day_of_month != 0:
        # starting & ending date of the week
        start = initial_day_of_month - \
            timedelta(days=initial_day_of_month.weekday())
        end = start + timedelta(days=5)

        # if Starting date is in previous month then changing it into first date of given_date month
        if start.month < end.month:
            start = initial_day_of_month

        # if Ending date is in next month then changing it into last date of given_date month
        if next_month.month == end.month:
            end = last_day_of_month
            last_day_of_month = 0

        # starting & ending date is between the given_date month then append to list
        if start.month == dt.month:
            list_of_dates.append((start, end))

        # Changing date to next week
        initial_day_of_month = end + timedelta(days=2)

    # Fetching attendance Present & Absent count
    for iteration, date1 in enumerate(list_of_dates):
        # if attendance data should be between start date and end date for generating data within that week
        class_present = AttendanceModel.objects.filter(
            attendance_id__date__gte=(date1[0]), attendance_id__date__lte=date1[1], status="Present").count()
        class_absent = AttendanceModel.objects.filter(
            attendance_id__date__gte=(date1[0]), attendance_id__date__lte=date1[1], status="Absent").count()
        dates.append("Week " + str(iteration + 1))
        # storing total present of particular class
        present.append(class_present)
        # storing total absent of particular class
        absent.append(class_absent)

    return JsonResponse({
        'labels': dates,
        'present': present,
        'absent': absent,
    })


# Class-wise Attendance stacked-bar chart (month)
def all_month_calender(request):
    dates = []
    present = []
    absent = []
    list_of_dates = []
    given_date = request.POST.get('current_date', date.today())

    # change str of date to date type
    dt = datetime.strptime(str(given_date), '%Y-%m-%d').date()

    for x in range(1, 13):
        end = last_day_of_month(dt.replace(month=x))
        start = end.replace(day=1)
        list_of_dates.append((start, end))

    # Fetching attendance Present & Absent count
    for date1 in list_of_dates:
        # if attendance data should be between start date and end date for generating data within that month
        class_present = AttendanceModel.objects.filter(
            attendance_id__date__gte=(date1[0]), attendance_id__date__lte=date1[1], status="Present").count()
        class_absent = AttendanceModel.objects.filter(
            attendance_id__date__gte=(date1[0]), attendance_id__date__lte=date1[1], status="Absent").count()
        dates.append(date1[0].strftime("%b"))
        # storing total present of particular class
        present.append(class_present)
        # storing total absent of particular class
        absent.append(class_absent)

    return JsonResponse({
        'labels': dates,
        'present': present,
        'absent': absent,
    })


# Overall Percentage
def all_per():
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
def all_tot():
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
    if request.method == "GET":
        # Percentage of All Data
        overall_percentage = all_per()
        # Student, Staff, Present, Absent
        total_stud_count, staff_count, Present_count, Absent_count = all_tot()

    elif request.method == "POST":
        classroom_id = request.POST.get('class_id', None)
        current_date = request.POST.get('current_date', None)

        Attendance_id_obj = AttendanceIdModel.objects.filter(
            classroom__id__icontains=classroom_id, date__icontains=current_date)
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
        'overall_perc': overall_percentage,
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
