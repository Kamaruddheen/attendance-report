from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import datetime
from subject.models import SubjectModel, HourModel
from timetable.models import TimetablesetModel, TimetableModel
from attendancess.models import AttendanceModel, AttendanceIdModel
from classroom.models import ClassroomModel

# List of Class they are going


class ClassesView(LoginRequiredMixin, View):
    def get(self, request):
        date = request.GET.get('date', 0)

        # Finding date
        if date == 0:
            # Set date Today by default
            date = datetime.date.today()
        else:
            # Getting the date from user
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        # Finding the Day
        day = date.strftime("%A")

        days = {
            "Sunday": 0,
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6
        }
        day = days[day]

        # Get all the active time tables and extract the classes
        active_sets = []
        time_table_sets = TimetablesetModel.objects.all()
        # print(type(time_table_sets))
        for set in time_table_sets:
            # Date should be between from & to date of Timetable
            if set.from_date <= date <= set.to_date:
                # Getting the currently active timetable of user requested date
                active_sets.append(set)  # Storing in active set
        classes = []

        # active_sets are in filter of Timetablemodel
        handled_by = SubjectModel.objects.filter(handled_by=request.user)
        for subject in handled_by:
            if subject.hour:
                classes.append(TimetableModel.objects.filter(
                    set_name__in=active_sets, day=day, subject__id=subject.hour.id).order_by('hour'))

        date = date.strftime("%Y-%m-%d")
        request.session['date'] = date

        data = []
        # Redirecting page for Attendance Entry & View Page
        for clas in classes:
            for c in clas:
                sub = get_object_or_404(
                    SubjectModel, hour=c.subject, handled_by=request.user)
                if AttendanceIdModel.objects.filter(date=date, hour_fk=c.subject, subject=sub).exists():
                    # True = Posted
                    data.append((c, True))
                else:
                    # False = Not Posted yet
                    data.append((c, False))

        context = {
            "data": data,
            "date": date
        }
        return render(request, 'attendancess/classes.html', context)


class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, hour_id, hour_number):

        hour = get_object_or_404(HourModel, pk=hour_id)
        subject = get_object_or_404(
            SubjectModel, hour=hour, handled_by=request.user)
        classroom = get_object_or_404(ClassroomModel, id=hour.classroom.id)

        date = request.GET.get('date', 0)
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        day = date.strftime("%A")

        days = {
            "Sunday": 0,
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6
        }
        day = days[day]

        # Get all the active time tables and extract the classes
        active_sets = []
        time_table_sets = TimetablesetModel.objects.all()
        # print(type(time_table_sets))
        for set in time_table_sets:
            # Date should be between from & to date of Timetable
            if set.from_date <= date <= set.to_date:
                # Getting the currently active timetable of user requested date
                active_sets.append(set)  # Storing in active set

        if not TimetableModel.objects.filter(
                set_name__in=active_sets, day=day, subject=hour, hour=hour_number).exists():
            date = date.strftime("%Y-%m-%d")
            request.session['date'] = date

            messages.info(
                request, 'The given Hour doesn\'t match the your timetable')

            return redirect(reverse("attendancess:classes")+"?date="+date, permanent=True)

        # Fetching students details
        if hour.hour_type == 'sel':
            # For Selective class Fetching student details from Subject
            students = subject.students.all().order_by("username")
        elif hour.hour_type == 'reg' or hour.hour_type == 'lab':
            # For Regular & Lab class Fetching student details from Classroom
            students = classroom.students.all().order_by("username")

        date = date.strftime("%Y-%m-%d")
        request.session['date'] = date

        # Checking already Posted or Not
        if AttendanceIdModel.objects.filter(date=date, hour_fk=hour,
                                            subject=subject, hour=hour_number).exists():
            # if already posted redirect them to attendance class page
            messages.info(
                request, 'You have already entered attendance for this Date')

            return redirect(reverse("attendancess:classes")+"?date="+date, permanent=True)

        # Convert date from "yyyy-mm-dd" format to "dd-mm-yyyy" format.
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        date = date.strftime("%d-%m-%Y")

        context = {
            'hour_number': hour_number,
            'students': students,
            'subject': subject,
            'hour': hour,
            'date': date
        }
        return render(request, 'attendancess/attendance.html', context)

    def post(self, request, hour_id, hour_number):

        hour = get_object_or_404(HourModel, pk=hour_id)
        subject = get_object_or_404(
            SubjectModel, hour=hour, handled_by=request.user)
        classroom = get_object_or_404(ClassroomModel, id=hour.classroom.id)

        # Checking whether the subject id is belonging to the current user
        # if not subject.handled_by == request.user:
        #     context = {
        #         "msg": "You are not allowed to view this page."
        #     }
        #     return render(request, "error.html", context)

        # students = subject.students.all().order_by("username")

        # Fetching students details
        if hour.hour_type == 'sel':
            # For Selective class Fetching student details from Subject
            students = subject.students.all().order_by("username")
        elif hour.hour_type == 'reg' or hour.hour_type == 'lab':
            # For Regular & Lab class Fetching student details from Classroom
            students = classroom.students.all().order_by("username")

        date = request.session['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        # Checking already Posted or Not
        if not AttendanceIdModel.objects.filter(date=date, hour_fk=hour,
                                                subject=subject, hour=hour_number).exists():
            a = AttendanceIdModel(date=date, hour_fk=hour,
                                  subject=subject, hour=hour_number)
            a.save()

            attendance_id = a.id
        else:
            # if already posted redirect them to attendance class page
            messages.info(
                request, 'You have already entered attendance for this Date')

            return redirect(reverse("attendancess:classes")+"?date="+date, permanent=True)

        # If the toggle button is on (present), the value will be in the request.POST .
        for student in students:
            if student.username in request.POST:
                AttendanceModel(attendance_id=attendance_id,
                                rollno=student.username, status="Present").save()
            else:
                AttendanceModel(attendance_id=attendance_id,
                                rollno=student.username, status="Absent").save()

        date = request.session['date']
        del request.session['date']

        return redirect(reverse("attendancess:classes")+"?date="+date, permanent=True)


class CheckAttendanceView(LoginRequiredMixin, View):
    def get(self, request):

        hour_id = request.GET.get('id')
        date = request.GET.get('date')
        hour_number = request.GET.get('hournumber')
        subject = get_object_or_404(
            SubjectModel, hour=hour_id, handled_by=request.user)
        if hour_id is None or date is None or hour_number is None:
            raise Http404("The required arguments are missing")

        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        attendance_id = get_object_or_404(
            AttendanceIdModel, hour_fk=hour_id, subject=subject, date=date, hour=hour_number)

        date = attendance_id.date.strftime("%d-%m-%Y")

        # Checking whether the subject id is belonging to the current user
        if not attendance_id.subject.handled_by == request.user:
            raise Http404("You are not allowed to view this page.")

        data = AttendanceModel.objects.filter(
            attendance_id=attendance_id.id).order_by('rollno')

        context = {
            'hour_number': hour_number,
            'hour': subject,
            "data": data,
            "date": date,
            "attendance_id": attendance_id
        }
        return render(request, 'attendancess/check_attendance.html', context)
