from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from classroom.models import ClassroomModel

def is_hod(function):
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated:
			if hasattr(request.user,'staffmodel') and request.user.staffmodel.is_hod:
				return function(request,*args,**kwargs)
			else:
				messages.info(request,'Not Authorized')
				prev_url = request.META.get('HTTP_REFERER')
				cur_url = request.get_full_path()
				print(prev_url)
				if prev_url:
					redirect_url = 'homepage' if cur_url in prev_url else prev_url
				else:
					redirect_url = 'homepage'
				print(redirect_url)
				return redirect(redirect_url or 'homepage',)
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
				prev_url = request.META.get('HTTP_REFERER')
				cur_url = request.get_full_path()
				print(prev_url)
				if prev_url:
					redirect_url = 'homepage' if cur_url in prev_url else prev_url
				else:
					redirect_url = 'homepage'
				print(redirect_url)
				return redirect(redirect_url or 'homepage',)
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
				prev_url = request.META.get('HTTP_REFERER')
				cur_url = request.get_full_path()
				print(prev_url)
				if prev_url:
					redirect_url = 'homepage' if cur_url in prev_url else prev_url
				else:
					redirect_url = 'homepage'
				print(redirect_url)
				return redirect(redirect_url or 'homepage',)
		else:
			return redirect(redirect('login').url+'?next='+request.path)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_hod_or_tutor(function):	# WARNING - use it only if you pass the classroom_id as id to the view function
	def wrap(request,id,*args,**kwargs):
		if request.user.is_authenticated:
			u = request.user
			class_obj = get_object_or_404(ClassroomModel,id=id)
			if u.staffmodel.is_hod or class_obj.tutor == u:
				return function(request,id,*args,**kwargs)
			else:
				prev_url = request.META.get('HTTP_REFERER')
				cur_url = request.get_full_path()
				print(prev_url)
				if prev_url:
					redirect_url = 'homepage' if cur_url in prev_url else prev_url
				else:
					redirect_url = 'homepage'
				print(redirect_url)
				messages.info(request,'Only the Tutor of {} and HoD have access.'.format(str(class_obj).upper()))
				return redirect(redirect_url or 'homepage',)
		else:
			return redirect(redirect('login').url+'?next='+request.path,permanent=True)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap