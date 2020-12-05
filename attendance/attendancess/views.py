from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
from subject.models import SubjectModel
from timetable.models import TimetablesetModel, TimetableModel

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
        
        context = {
            "classes" : classes,
            "date" : date
        }
        return render(request, 'attendance/classes.html', context)


class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, subject_id):

        students = SubjectModel.objects.get(id=subject_id).students.all()
        print(students)
        context = {
            'students' : students
        }
        return render(request, 'attendance/attendance.html', context)
