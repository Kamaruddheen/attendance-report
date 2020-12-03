from django.shortcuts import render
from django.contrib import messages
from .forms import ClassroomForm
from .models import ClassroomModel
# Create your views here.
def CreateClass(request):
    if request.method=="POST":
        ClassroomObject=ClassroomForm(request.POST)
        if ClassroomObject.is_valid():
            ClassroomObject.save()
            #tuple is faster than lists
            all_classrooms=ClassroomModel.objects.all()
            messages.success(request,"Classroom created")
            return render(request,'classroom/ClassRoom.html',{'all_classrooms':all_classrooms})
        all_classrooms=ClassroomModel.objects.all()
        errors="having"
        return render(request,'classroom/ClassRoom.html',{'all_classrooms':all_classrooms,'form':ClassroomObject,'errors':errors})
    else:
        all_classrooms=ClassroomModel.objects.all()
        ClassroomObject=ClassroomForm()
        return render(request,'classroom/ClassRoom.html',{'form':ClassroomObject,'all_classrooms':all_classrooms})