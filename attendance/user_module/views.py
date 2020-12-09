from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateStaffForm, EditStaffForm
from .models import StaffModel
from .decorators import is_hod,is_hod_or_self

# Create your views here.

@login_required
@is_hod
def createstaffview(request):
	myForm = CreateStaffForm(request.POST or None)
	if myForm.is_valid():
		form_obj = myForm.save(commit=False)
		form_obj.user_type = 2
		form_obj.save()
		messages.success(request,'Staff Created Successfully')
		return redirect('create_staff')
	context = {
		'form':myForm,
	}
	return render(request,'user_module/createstaff.html',context=context)

@login_required
@is_hod
def managestaffview(request):
	staff_obj = StaffModel.objects.filter(is_hod=False)
	context = {
		'staffs':staff_obj,
	}
	return render(request,'user_module/managestaff.html',context=context)

@login_required
@is_hod_or_self
def staffdetailview(request,id):
	staff_obj = get_object_or_404(StaffModel,id=id)
	myForm = EditStaffForm(request.POST or None,instance=staff_obj.user)
	if myForm.is_valid():
		myForm.save()
	context = {
		'staff':staff_obj,
		'form':myForm,
	}
	return render(request,'user_module/staff_detail.html',context=context)