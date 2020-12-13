import os
from django.conf import settings
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
        # image
        files = os.listdir(os.path.join(
            settings.STATIC_DIR, "static\\img\\classrooms\\"))
        mylist = zip(all_classrooms, files)

        # if no. of subjects is greater than the no. of images
        if len(all_classrooms) > len(files):
            value = None
            value = len(all_classrooms) - len(files)
            for i in range(0, value):
                files.append("classroom11.jpg")
            # if no. of images is greater than the no. of subjects
        elif len(files) > len(all_classrooms):
            pass
        context = {
            'form': ClassroomObject,
            'mylist': mylist
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
