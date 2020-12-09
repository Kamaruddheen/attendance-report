from django.shortcuts import render,redirect

from .forms import CreateSubjectForm
from .models import SubjectModel

# Create your views here.

def SubjectListView(request):
	sub_obj = SubjectModel.objects.all()
	context = {
		'subjects':sub_obj,
	}
	return render(request,'subject/subject_list.html',context=context)

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
