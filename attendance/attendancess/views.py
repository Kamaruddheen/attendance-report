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
        # Get all the subjects of the current user.
        subjects = SubjectModel.objects.filter(handled_by=request.user).values_list('hour_name', flat=True)
        print(subjects)

        # Get all the active time tables and extract the classes
        active_sets = []
        time_table_sets = TimetablesetModel.objects.all()
        for set in time_table_sets:
            if set.from_date <= date <= set.to_date:
                active_sets.append(set)

        classes = TimetableModel.objects.filter(set_name__in = time_table_sets, day=day, subject__in=subjects)

        for clas in classes:
            year = clas.set_name.classroom.year 
            if year == 1:
                clas.set_name.classroom.year = "I"
            elif year == 2:
                clas.set_name.classroom.year = "II"
            elif year == 3:
                clas.set_name.classroom.year = "III"
            else:
                clas.set_name.classroom.year = "error"

        date = date.strftime("%Y-%m-%d")
        

        context = {
            "classes" : classes,
            "date" : date
        }
        return render(request, 'attendance/classes.html', context)
