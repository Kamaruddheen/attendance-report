from django.shortcuts import render
from .forms import TimetableForm
# Create your views here.
def createtimetable(request,id):
    t=TimetableForm(request.POST or None,id=id)
    return render(request,'timetable/timetable.html',{'t':t})
    
