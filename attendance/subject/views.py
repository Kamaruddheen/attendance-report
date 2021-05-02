from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django import forms
import os

from .forms import CreateSubjectForm, CreateHourForm, HourFormSet, SubjectAddStudentsForm
from .models import SubjectModel, HourModel
from classroom.models import ClassroomModel


def HourListView(request, class_id):
    class_obj = get_object_or_404(ClassroomModel, id=class_id)
    hour_obj = HourModel.objects.filter(classroom=class_obj)
    sub_count = []
    for hour in hour_obj:
        count = SubjectModel.objects.filter(hour=hour).count()
        sub_count.append(count)
    hour_obj = zip(hour_obj, sub_count)
    context = {
        'class_obj': class_obj,
        'hour_obj': hour_obj,
        # 'sub_count': sub_count,
    }
    return render(request, 'subject/HourList.html', context=context)


def HourDetailView(request, class_id, hour_id):
    hour_obj = get_object_or_404(HourModel, id=hour_id, classroom__id=class_id)
    subjects = SubjectModel.objects.filter(hour=hour_obj)
    files = os.listdir(os.path.join(
        settings.STATIC_DIR, "static\\img\\books\\"))
    mylist = zip(subjects, files)

    # if no. of subjects is greater than the no. of images
    if len(subjects) > len(files):
        value = None
        value = len(subjects) - len(files)
        for i in range(0, value):
            files.append("book8.jpg")
    # if no. of images is greater than the no. of subjects
    elif len(files) > len(subjects):
        pass

    context = {
        'hour_obj': hour_obj,
        'mylist': mylist,
    }
    return render(request, 'subject/HourDetail.html', context=context)


def HourEditView(request, class_id, hour_id):
    class_obj = get_object_or_404(ClassroomModel, id=class_id)
    hour_obj = get_object_or_404(HourModel, id=hour_id, classroom__id=class_id)
    SubjectFormset = forms.inlineformset_factory(HourModel, SubjectModel, fields=(
        'sub_name', 'handled_by','sub_code'), formset=HourFormSet, extra=0, can_delete=False)
    if request.method == "POST":
        formset = SubjectFormset(
            request.POST, instance=hour_obj, prefix="subject_edit")
        if formset.is_valid():
            formset.save()
            return redirect(hour_obj)
        else:
            pass
            # print('not valid')
    else:
        formset = SubjectFormset(instance=hour_obj, prefix="subject_edit")
    context = {
        'class_obj': class_obj,
        'formset': formset,
    }
    return render(request, 'subject/HourEdit.html', context=context)


def HourAddStudView(request, class_id, hour_id, sub_id):
    class_obj = get_object_or_404(ClassroomModel, id=class_id)
    sub_obj = get_object_or_404(
        SubjectModel, id=sub_id, hour__id=hour_id, hour__classroom__id=class_id)
    sub_list = SubjectModel.objects.filter(hour=sub_obj.hour)
    myForm = SubjectAddStudentsForm(
        request.POST or None, instance=sub_obj, request=request, sub_list=sub_list)
    if myForm.is_valid():
        myForm.save()
    context = {
        'class_obj': class_obj,
        'sub_obj': sub_obj,
        'form': myForm,
    }
    return render(request, 'subject/HourAddStudent.html', context=context)


def create_hour_view(request, class_id):
    class_obj = get_object_or_404(ClassroomModel, id=class_id)
    SubjectFormset = forms.formset_factory(
        CreateSubjectForm, extra=0, min_num=1, validate_min=True)
    if request.method == "POST":
        myForm = CreateHourForm(request.POST)
        formset = SubjectFormset(request.POST, prefix='subject_form')
        if all([myForm.is_valid(), formset.is_valid()]):
            hour_obj = myForm.save(commit=False)
            hour_obj.classroom = class_obj
            hour_obj.save()
            # print(hour_obj.id)
            for inline_form in formset:
                if inline_form.cleaned_data:
                    sub_obj = inline_form.save(commit=False)
                    sub_obj.hour = hour_obj
                    sub_obj.save()
                    # print(sub_obj)
                else:
                    pass
                    # print('sub is not valid')
            # print('its all valid')
            messages.success(request, 'Created Successfully')

            myForm = CreateHourForm()
            formset = SubjectFormset(prefix='subject_form')

            context = {
                'class_obj': class_obj,
                'form': myForm,
                'formset': formset,
            }

            return render(request, 'subject/create_hour.html', context=context)
        else:
            pass
            # print('its not valid')
    else:
        myForm = CreateHourForm()
        formset = SubjectFormset(prefix='subject_form')
    context = {
        'class_obj': class_obj,
        'form': myForm,
        'formset': formset,
    }
    return render(request, 'subject/create_hour.html', context=context)


# def SubjectListView(request):
#     sub_obj = SubjectModel.objects.all()
#     files = os.listdir(os.path.join(
#         settings.STATIC_DIR, "static\\img\\books\\"))
#     mylist = zip(sub_obj, files)

#     # if no. of subjects is greater than the no. of images
#     if len(sub_obj) > len(files):
#         value = None
#         value = len(sub_obj) - len(files)
#         for i in range(0, value):
#             files.append("book8.jpg")
#         # if no. of images is greater than the no. of subjects
#     elif len(files) > len(sub_obj):
#         pass

#     context = {
#         'mylist': mylist
#     }
#     return render(request, 'subject/subject_list.html', context=context)


# def SubjectCreateView(request):

#     staff = get_object_or_404(StaffModel, user_id=request.user.id)
#     myForm = CreateSubjectForm(request.POST or None, staff=staff)
#     if myForm.is_valid():
#         myForm.save()
#         return redirect('subject:subject_list')
#     context = {
#         'form': myForm,
#     }
#     return render(request, 'subject/subject_create.html', context=context)


# def SubjectDetailView(request, id):
#     subject = get_object_or_404(SubjectModel, id=id)
#     context = {
#         "subject": subject
#     }
#     return render(request, 'subject/subject_detail.html', context=context)


# class SubjectEditView(LoginRequiredMixin, View):

#     def get(self, request, id):

#         subject = get_object_or_404(SubjectModel, id=id)
#         staff = StaffModel.objects.get(user=request.user)
#         if staff.is_hod or subject.classroom.tutor != request.user:
#             raise Http404("You are not allowed to view this page.")

#         form = CreateSubjectForm(instance=subject, staff=staff)
#         context = {
#             "form": form
#         }
#         return render(request, 'subject/subject_edit.html', context)

#     def post(self, request, id):

#         subject = get_object_or_404(SubjectModel, id=id)
#         staff = StaffModel.objects.get(user=request.user)
#         if staff.is_hod or subject.classroom.tutor != request.user:
#             raise Http404("You are not allowed to view this page.")

#         form = CreateSubjectForm(request.POST or None,
#                                  instance=subject, staff=staff)
#         if form.is_valid():
#             form.save()
#             return redirect("subject:subject_list", permanent=True)
#         context = {
#             "form": form
#         }
#         return render(request, "subject/subject_edit.html", context)


# class SubjectDeleteView(LoginRequiredMixin, View):
#     def get(self, request, id):
#         subject = get_object_or_404(SubjectModel, id=id)
#         is_hod = StaffModel.objects.get(user=request.user).is_hod
#         if is_hod or subject.classroom.tutor != request.user:
#             raise Http404("You are not allowed to view this page.")

#         subject.delete()
#         return redirect("subject:subject_list", permanent=True)
