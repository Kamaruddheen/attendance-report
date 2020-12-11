from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import ClassroomForm
from .models import ClassroomModel


def CreateClass(request):
    if request.method == "POST":
        ClassroomObject = ClassroomForm(request.POST)
        if ClassroomObject.is_valid():
            ClassroomObject.save()
            all_classrooms = ClassroomModel.objects.all()
            messages.success(request, "Classroom created")
            return render(request, 'classroom/view_and_create_classroom.html', {'all_classrooms': all_classrooms})
        all_classrooms = ClassroomModel.objects.all()
        context = {
            'all_classrooms': all_classrooms,
            'form': ClassroomObject
        }
        return render(request, 'classroom/view_and_create_classroom.html', context=context)
    else:
        all_classrooms = ClassroomModel.objects.all()
        ClassroomObject = ClassroomForm()
        context = {
            'form': ClassroomObject,
            'all_classrooms': all_classrooms
        }
        return render(request, 'classroom/view_and_create_classroom.html', context=context)


def editclass(request, id):
    get_obj = get_object_or_404(ClassroomModel, id=id)
    editclass = ClassroomForm(request.POST or None, instance=get_obj)
    if request.method == 'POST':
        if editclass.is_valid():
            editclass.save()
    context = {
        'get_obj': get_obj,
        'editclass': editclass
    }
    return render(request, 'classroom/edit_classroom.html', context=context)
