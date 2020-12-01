from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateStaffForm

# Create your views here.

@login_required
def createstaffview(request):
	myForm = CreateStaffForm(request.POST or None)
	if myForm.is_valid():
		form_obj = myForm.save(commit=False)
		form_obj.user_type = 2
		form_obj.save()
		messages.success(request,'Staff Created Successfully')
		return redirect('homepage')
	context = {
		'form':myForm,
	}
	return render(request,'user_module/createstaff.html',context=context)
	