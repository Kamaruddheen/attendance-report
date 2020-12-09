from django.shortcuts import render, redirect
from django.conf import settings
import os

from .forms import CreateSubjectForm
from .models import SubjectModel

def SubjectListView(request):
    sub_obj = SubjectModel.objects.all()
    files = os.listdir(os.path.join(
        settings.STATIC_DIR, "static\\img\\books\\"))
    mylist = zip(sub_obj, files)

    # if no. of subjects is greater than the no. of images
    if len(sub_obj) > len(files):
        value = None
        value = len(sub_obj) - len(files)
        for i in range(0, value):
            files.append("book1.jpg")
        # if no. of images is greater than the no. of subjects
    elif len(files) > len(sub_obj):
        pass

    context = {
        'mylist': mylist
    }
    return render(request, 'subject/subject_list.html', context=context)

def SubjectCreateView(request):
	myForm = CreateSubjectForm(request.POST or None)
	if myForm.is_valid():
		myForm.save()
		return redirect('subject:subject_list')
	context = {
		'form':myForm,
	}
	return render(request,'subject/subject_create.html',context=context)

def SubjectDetailView(request,id):
	context = {}
	return render(request,'subject/subject_detail.html',context=context)
