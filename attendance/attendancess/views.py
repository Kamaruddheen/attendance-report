from django.shortcuts import render, redirect
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
        date = request.GET.get('date',0)
        
        if date == 0:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
        day = date.strftime("%A")

        # Get all the active time tables and extract the classes
        active_sets = []
        time_table_sets = TimetablesetModel.objects.all()
        for set in time_table_sets:
            if set.from_date <= date <= set.to_date:
                active_sets.append(set)

        classes = TimetableModel.objects.filter(set_name__in = time_table_sets, day=day, subject__handled_by = request.user).order_by('hour')

        date = date.strftime("%Y-%m-%d")
        request.session['date'] = date
        
        context = {
            "classes" : classes,
            "date" : date
        }
        return render(request, 'attendancess/classes.html', context)


class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, subject_id):
        
        students = SubjectModel.objects.get(id=subject_id).students.all().order_by("username")
        print(students)
        print(request.session.get('date',0))
        context = {
            'students' : students
        }
        return render(request, 'attendancess/attendance.html', context)

    def post(self, request, subject_id):

        subject = SubjectModel.objects.get(id=subject_id)
        students = subject.students.all().order_by("username")
        
        date = request.session['date']
        date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
        
        a = AttendanceIdModel(date = date,
                            subject = subject,
                            handled_by = "NA",
        )
        a.save()

        attendance_id = a.id

        # If the toggle button is on(present), the value will be in the request.POST .
        for student in students:
            if student.username in request.POST:
                AttendanceModel(attendance_id=attendance_id, rollno=student.username, status="Present").save()
            else:
                AttendanceModel(attendance_id=attendance_id, rollno=student.username, status="Absent").save()
                

        date = request.session['date']
        del request.session['date']

        return redirect(reverse("attendancess:classes")+"?date="+date, permanent=True)
