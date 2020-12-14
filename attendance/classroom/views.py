import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory, inlineformset_factory
from .forms import ClassroomForm, AddStudentCSVForm, AddStudentForm, BaseStudentFormSet
from .models import ClassroomModel

import csv, io, json
from django.http import JsonResponse
from user_module.models import User
from user_module.decorators import *


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

@is_staff
def ManageStudents(request,id):
    class_obj = get_object_or_404(ClassroomModel,id=id)
    if request.method == "POST":
        username = request.POST.get('username',None)
        stds_obj = get_object_or_404(class_obj.students,username=username)
        if stds_obj.user_type == 3:
            stds_obj.delete()
            messages.success(request,"Student {} deleted Successfully".format(username))
        return redirect('classroom:manage_students',id=id,permanent=True)
    stds_obj = class_obj.students.order_by('username').values('username','first_name','last_name','email','id')
    for i in stds_obj:
        i['username_error_msg'] = "";
        i['username_error'] = False;
        i['first_name_error_msg'] = "";
        i['first_name_error'] = False;
        i['email_error_msg'] = "";
        i['email_error'] = False;
        i['edit'] = False;
    context = {
        'class_obj': class_obj,
        'stds_obj': json.dumps(list(stds_obj)),
    }
    return render(request,'classroom/manage_students.html',context=context)

@is_hod_or_tutor
def ajax_update_student(request,id):
    data = {"is_working":True}
    if request.method == "POST" and request.is_ajax():
        id = request.POST.get('obj[id]',None)
        index = request.POST.get('index',None)
        data = {
            'username': request.POST.get('obj[username]',None),
            'first_name': request.POST.get('obj[first_name]',None),
            'last_name': request.POST.get('obj[last_name]',None),
            'email': request.POST.get('obj[email]',None)
        }
        if User.objects.filter(id=id).exists() and index:
            print('exists')
            myform = AddStudentForm(data,instance=User.objects.get(id=id))
            if myform.is_valid():
                print('valid')
                myform.save()
                resp = {
                    "valid": True,
                    "updated": True,
                    "index": index,
                }
            else:
                print('not valid')
                print(myform.errors.as_json())
                resp = {
                    "valid": False,
                    "errors": myform.errors.as_json(),
                    "index": index,
                }
            return JsonResponse(resp,safe=False)
        else:
            print('does not exist')
            response =  JsonResponse({'status':'ID Not Found'})
            response.status_code = 404
            return response
    response =  JsonResponse({'status':'Not Authorized'})
    response.status_code = 404
    return response

@is_hod_or_tutor
def AddStudents(request,id):
    class_obj = get_object_or_404(ClassroomModel,id=id)
    csv_form = AddStudentCSVForm()
    initial = []
    StudentFormSet = modelformset_factory(User,formset=BaseStudentFormSet,form=AddStudentForm)
    formset = StudentFormSet(queryset=User.objects.none())
    if request.method == "POST" and request.POST.get('add_stud_csv_form',False):
        csv_form = AddStudentCSVForm(request.POST,request.FILES)
        if csv_form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'Not a csv file')
            else:
                # print(csv_file)
                io_string = io.StringIO(csv_file.read().decode())
                csv_reader = csv.DictReader(io_string)
                print(csv_reader.fieldnames)
                for i,v in enumerate(csv_reader.fieldnames):
                    csv_reader.fieldnames[i] = v.lower()
                print(csv_reader.fieldnames)
                for row in csv_reader:
                    if row.get('username',False):
                        initial.append(row)
                    else:
                        print(row)
                        initial.append({'a':'a'})
                        messages.info(request,"The column header should have username")
                        break
                # print(initial)
                # print(len(initial))
                StudentFormSet = modelformset_factory(User,fields=('username','email','first_name','last_name'),formset=BaseStudentFormSet,form=AddStudentForm,extra=len(initial))
                formset = StudentFormSet(initial=initial)
    elif request.method == "POST" and request.POST.get('add_stud_form',False):
        formset = StudentFormSet(request.POST)
        print('atleat it came')
        if formset.is_valid():
            print('valid')
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user_type = 3
                instance.is_active = False
            user_obj = User.objects.bulk_create(instances)
            user_obj = User.objects.filter(email__in=(ins.email for ins in instances))
            class_obj.students.add(*(user_obj))
            messages.success(request,'Student Added Successfully')
            return redirect('classroom:manage_students',id=class_obj.id)
    context = {
        'csv_form': csv_form,
        'formset': formset,
    }
    return render(request,'classroom/add_students.html',context=context)