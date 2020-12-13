from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
import os

from .forms import CreateSubjectForm
from .models import SubjectModel
from user_module.models import StaffModel


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
            files.append("book8.jpg")
        # if no. of images is greater than the no. of subjects
    elif len(files) > len(sub_obj):
        pass

    context = {
        'mylist': mylist
    }
    return render(request, 'subject/subject_list.html', context=context)


def SubjectCreateView(request):

    staff = get_object_or_404(StaffModel, user_id=request.user.id)
    myForm = CreateSubjectForm(request.POST or None, staff=staff)
    if myForm.is_valid():
        myForm.save()
        return redirect('subject:subject_list')
    context = {
        'form': myForm,
    }
    return render(request, 'subject/subject_create.html', context=context)


def SubjectDetailView(request, id):
    subject = get_object_or_404(SubjectModel, id=id)
    context = {
        "subject": subject
    }
    return render(request, 'subject/subject_detail.html', context=context)


class SubjectEditView(LoginRequiredMixin, View):

    def get(self, request, id):

        subject = get_object_or_404(SubjectModel, id=id)
        staff = StaffModel.objects.get(user=request.user)
        if staff.is_hod or subject.classroom.tutor != request.user:
            raise Http404("You are not allowed to view this page.")

        form = CreateSubjectForm(instance=subject, staff=staff)
        context = {
            "form": form
        }
        return render(request, 'subject/subject_edit.html', context)

    def post(self, request, id):

        subject = get_object_or_404(SubjectModel, id=id)
        staff = StaffModel.objects.get(user=request.user)
        if staff.is_hod or subject.classroom.tutor != request.user:
            raise Http404("You are not allowed to view this page.")

        form = CreateSubjectForm(request.POST or None,
                                 instance=subject, staff=staff)
        if form.is_valid():
            form.save()
            return redirect("subject:subject_list", permanent=True)
        context = {
            "form": form
        }
        return render(request, "subject/subject_edit.html", context)


class SubjectDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        subject = get_object_or_404(SubjectModel, id=id)
        is_hod = StaffModel.objects.get(user=request.user).is_hod
        if is_hod or subject.classroom.tutor != request.user:
            raise Http404("You are not allowed to view this page.")

        subject.delete()
        return redirect("subject:subject_list", permanent=True)
