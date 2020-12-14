from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import User
from classroom.models import ClassroomModel

def is_hod(function):
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated:
			if hasattr(request.user,'staffmodel') and request.user.staffmodel.is_hod:
				return function(request,*args,**kwargs)
			else:
				messages.info(request,'Not Authorized')
				return redirect('homepage')
		else:
			return redirect(redirect('login').url+'?next='+request.path)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_staff(function):
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 2:
				return function(request,*args,**kwargs)
			else:
				messages.info(request,'Not Authorized')
				return redirect('homepage')
		else:
			return redirect(redirect('login').url+'?next='+request.path)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_hod_or_self(function):
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated:
			u = request.user
			if (hasattr(u,'staffmodel') and u.staffmodel.is_hod) or (hasattr(u,'staffmodel') and u.staffmodel.id == kwargs['id']):
				return function(request,*args,**kwargs)
			else:
				messages.info(request,'Not Authorized')
				print(kwargs['id'],u.id)
				print(type(kwargs['id']))
				return redirect('homepage')
		else:
			return redirect(redirect('login').url+'?next='+request.path)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_hod_or_tutor(function):
	def wrap(request,id,*args,**kwargs):
		if request.user.is_authenticated:
			u = request.user
			class_obj = get_object_or_404(ClassroomModel,id=id)
			if u.staffmodel.is_hod or class_obj.tutor == u:
				return function(request,id,*args,**kwargs)
			else:
				messages.info(request,'Only the Tutor of {} and HoD have access'.format(class_obj))
				return redirect(request.META.get('HTTP_REFERER'))
		else:
			return redirect(redirect('login').url+'?next='+request.path)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap