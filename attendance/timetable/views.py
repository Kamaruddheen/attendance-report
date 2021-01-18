from django.contrib import messages
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import TimetableForm, TimetablesetForm, edit_timetableForm, choose_set_form
from .models import ClassroomModel, TimetableModel, TimetablesetModel, SubjectModel
import json
from datetime import date
from queryset_sequence import QuerySetSequence
# Create your views here.

# Create timetable


def createtimetable(request, class_id, set_id):
    if request.method == 'POST':
        # The below day variable is used twice always so that is declared and initialised here
        day = request.POST['day'] or 0
        if TimetableModel.objects.filter(set_name__id=set_id, day=day).exists():
            if day == 0:
                messages.error(request, "Please select a Day")
            else:
                messages.error(
                    request, "You already added timetable for this day. Go to \"Manage Timetable\" to edit")
            c_object = get_object_or_404(ClassroomModel, id=class_id)
            t = TimetableForm(request.POST or None, initial={
                              'set_name': set_id}, c_object=c_object)
            return render(request, 'timetable/timetable.html', {'form': t, 'c_object': c_object, 'set_id': set_id})
        else:
            for i in range(1, 6):
                t_obj = TimetableModel()
                a = 's'+str(i)
                a = request.POST[a]
                # len(a) returns 0
                if len(a) == 0:
                    t_obj.subject = None
                else:
                    # foriegn key choices are stored as referenced objects but normal user defined choices are stored as the first element in the tuple defined
                    t_obj.subject = get_object_or_404(
                        SubjectModel, id=a)  # Subject gets initialized
                a = request.POST['set_name']
                t_obj.set_name = get_object_or_404(
                    TimetablesetModel, id=a)  # set name gets initialized
                t_obj.day = day  # day gets initialized
                t_obj.hour = i  # hour gets initialized
                t_obj.save()
            check = TimetableModel.objects.filter(set_name__id=set_id)
            # To check whether maximum limit of the timetable are entered or not
            if len(check) >= 30:
                messages.info(
                    request, 'You have filled all the 6 days for timetable')
                return redirect('timetable:showsubjects', class_id=class_id, set_id=set_id)
            messages.success(request, 'Your timetable stored successfully.')
            c_object = get_object_or_404(ClassroomModel, id=class_id)
            t = TimetableForm(initial={'set_name': set_id}, c_object=c_object)
            return render(request, 'timetable/timetable.html', {'form': t, 'c_object': c_object, 'set_id': set_id})
    else:
        c_object = get_object_or_404(ClassroomModel, id=class_id)
        t = TimetableForm(initial={'set_name': set_id}, c_object=c_object)
        return render(request, 'timetable/timetable.html', {'form': t, 'c_object': c_object, 'set_id': set_id})

# Create timetable set


def createtimetableset(request, class_id):
    c_object = get_object_or_404(ClassroomModel, id=class_id)
    t_set = TimetablesetForm(request.POST or None)
    if t_set.is_valid():
        t_set = t_set.save(commit=False)
        # The object returned by the save(commit=false) is the model instance not the form instance so we are able to access classroom field which is not included in the form
        t_set.classroom = c_object
        t_set.save()
        return redirect('timetable:setchoose', class_id=class_id)
    return render(request, 'timetable/timetableset.html', {'t_set': t_set, 'c_object': c_object})

# Choose your set


def setchoose(request, class_id):
    c_object = get_object_or_404(ClassroomModel, id=class_id)
    if TimetablesetModel.objects.filter(classroom=c_object).exists():
        today = date.today()
        t_set_particular = TimetablesetModel.objects.filter(classroom=c_object)
        a = t_set_particular.filter(to_date__gte=today).order_by('to_date')
        b = t_set_particular.filter(to_date__lt=today).order_by('-to_date')
        c = QuerySetSequence(a, b)
        # Order : future set,current set,past set
        choose_set_object = choose_set_form(t_set_particular=c)
        context = {
            'choose_set_object': choose_set_object,
            'c_object': c_object
        }
        return render(request, 'timetable/setchoose.html', context)
    t_set = TimetablesetForm()
    return render(request, 'timetable/timetableset.html', {'c_object': c_object, 't_set': t_set, 'No_set': 1})


"""  # Set info page


def set_info(request, class_id=None, set_id=None):
    c_object = get_object_or_404(ClassroomModel, id=class_id)
    s_object = get_object_or_404(TimetablesetModel, id=set_id)
    t_set = TimetablesetForm(request.POST or None, instance=s_object)
    if t_set.is_valid():
        t_set.save()
        messages.success(request, 'Changes made are saved')
    return render(request, 'timetable/set_info.html', {'c_object': c_object, 's_object': s_object, 't_set': t_set})"""

# Timetable show


def showsubjects(request, class_id, set_id):
    any_empty_subject = False
    where_to_redirect = TimetableModel.objects.filter(set_name__id=set_id)
    # To check whether any subject is in the timetable :
    if len(where_to_redirect) == 0:
        c_object = get_object_or_404(ClassroomModel, id=class_id)
        t = TimetableForm(initial={'set_name': set_id}, c_object=c_object)
        messages.error(request, 'No subjects created for this timetable yet')
        return render(request, 'timetable/timetable.html', {'form': t, 'c_object': c_object, 'set_id': set_id})
    # Code if subjects are present in the particular timetable :
    s_object = get_object_or_404(TimetablesetModel, id=set_id)
    c_object = get_object_or_404(ClassroomModel, id=class_id)
    # Subjects for the particular timetable
    all_subjects = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for i in range(1, 7):
        setsubjects = TimetableModel.objects.filter(
            set_name__id=set_id, day=i).order_by('hour')
        j = 1
        subject_list = []
        if len(setsubjects) == 0:
            all_subjects.append(['-', '-', '-', '-', '-'])
            any_empty_subject = True
            continue
        for s_in_t_object in setsubjects:
            if s_in_t_object.hour == j:
                subject_list.append(s_in_t_object)
                j += 1
        all_subjects.append(subject_list)
    # zip function combines the two iterator and returns the combined version of the iterator
    all_subjects = zip(all_subjects, days)
    subject_list = SubjectModel.objects.filter(classroom=c_object)
    edit_timetable = edit_timetableForm(
        subject_list=subject_list, initial={'set_name': s_object})
    return render(request, 'timetable/showsubjects.html', {'all_subjects': all_subjects, 'c_object': c_object, 's_object': s_object, 'edit_timetable': edit_timetable, 'is_empty': any_empty_subject})


def showsubjects1(request, class_id, set_id):
    s_object = get_object_or_404(TimetablesetModel, id=set_id)
    c_object = get_object_or_404(ClassroomModel, id=class_id)
    # Subjects for the particular timetable
    all_subjects = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for i in range(1, 7):
        setsubjects = TimetableModel.objects.filter(
            set_name__id=set_id, day=i).order_by('hour')
        j = 1
        subject_list = []
        if len(setsubjects) == 0:
            all_subjects.append(['----', '----', '----', '----', '----'])
            continue
        for s_in_t_object in setsubjects:
            if s_in_t_object.hour == j:
                subject_list.append(s_in_t_object)
                j += 1
        all_subjects.append(subject_list)
    # zip function combines the two iterator and returns the combined version of the iterator
    all_subjects = zip(all_subjects, days)
    data = render(request, 'timetable/showsubjects1.html',
                  {'all_subjects': all_subjects, 'c_object': c_object, 's_object': s_object})
    return HttpResponse(data)

# Edit subjects in the timetable


def edit_subjects(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data = data['subject_list']
        for i in data:
            subject_id = i[0]
            timetable_id = i[1]

            if subject_id == 'Free':
                s_object = None
            else:
                # Implicitly on the left hand side code , subject_id is converted as a integer when comparing with integer values
                s_object = get_object_or_404(SubjectModel, id=subject_id)

            t_object = get_object_or_404(TimetableModel, id=timetable_id)
            t_object.subject = s_object
            t_object.save()
        return HttpResponse("saved")
