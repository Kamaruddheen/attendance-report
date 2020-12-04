from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from .forms import ClassroomForm
from .models import ClassroomModel
# Create your views here.
def CreateClass(request):
    if request.method=="POST":
        ClassroomObject=ClassroomForm(request.POST)
        if ClassroomObject.is_valid():
            ClassroomObject.save()
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

def editclass(request,id):
    get_obj=get_object_or_404(ClassroomModel,id=id)
    editclass=ClassroomForm(request.POST or None,instance=get_obj)
    if request.method=='POST':
        if editclass.is_valid():
            editclass.save()
    return render(request,'classroom/editclass.html',{'get_obj':get_obj,'editclass':editclass})
