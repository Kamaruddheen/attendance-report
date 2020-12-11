from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
from subject.models import SubjectModel
from timetable.models import TimetablesetModel, TimetableModel
from attendancess.models import AttendanceModel, AttendanceIdModel

# Create your views here.


class ClassesView(LoginRequiredMixin, View):
    def get(self, request):
        date = request.GET.get('date', 0)

        if date == 0:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        day = date.strftime("%A")

        days = {
            "Monday" : 1,
            "Tuesday" : 2,
            "Wednesday" : 3,
            "Thursday" : 4,
            "Friday" : 5,
            "Saturday" : 6
        }
        day = days[day]
        print(day)

        # Get all the active time tables and extract the classes
        active_sets = []
        time_table_sets = TimetablesetModel.objects.all()
        for set in time_table_sets:
            if set.from_date <= date <= set.to_date:
                active_sets.append(set)

        classes = TimetableModel.objects.filter(
            set_name__in=time_table_sets, day=day, subject__handled_by=request.user).order_by('hour')

        date = date.strftime("%Y-%m-%d")
        request.session['date'] = date

        data = []
        for clas in classes:
            if AttendanceIdModel.objects.filter(date=date, subject=clas.subject).exists():
                data.append((clas, True))
            else:
                data.append((clas, False))

        context = {
            "data": data,
            "date": date
        }
        return render(request, 'attendancess/classes.html', context)


class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, subject_id):

        subject = get_object_or_404(SubjectModel, pk=subject_id)

        # Checking whether the subject id is belonging to the current user
        if not subject.handled_by == request.user:
            context = {
                "msg": "You are not allowed to view this page."
            }
            return render(request, "error.html", context)

        students = subject.students.all().order_by("username")

        context = {
            'students': students,
            'subject': subject
        }
        return render(request, 'attendancess/attendance.html', context)

    def post(self, request, subject_id):

        subject = get_object_or_404(SubjectModel, pk=subject_id)

        # Checking whether the subject id is belonging to the current user
        if not subject.handled_by == request.user:
            context = {
                "msg": "You are not allowed to view this page."
            }
            return render(request, "error.html", context)

        students = subject.students.all().order_by("username")

        date = request.session['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        a = AttendanceIdModel(date=date,
                              subject=subject,
                              )
        a.save()

        attendance_id = a.id

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

        subject_id = request.GET.get('id')
        subject = get_object_or_404(SubjectModel, pk=subject_id)
        date = request.GET.get('date')

        if subject_id is None or date is None:
            raise Http404("The required arguments are missing")

        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        attendance_id = get_object_or_404(
            AttendanceIdModel, subject__id=subject_id, date=date)

        # Checking whether the subject id is belonging to the current user
        if not attendance_id.subject.handled_by == request.user:
            raise Http404("You are not allowed to view this page.")

        data = AttendanceModel.objects.filter(
            attendance_id=attendance_id.id).order_by('rollno')

        context = {
            "data": data,
            "subject": subject
        }
        return render(request, 'attendancess/check_attendance.html', context)
