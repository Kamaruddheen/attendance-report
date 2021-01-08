from django.contrib import messages
from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render,get_object_or_404
from .forms import TimetableForm,TimetablesetForm,edit_timetableForm
from .models import ClassroomModel,TimetableModel,TimetablesetModel,SubjectModel
import json
# Create your views here.
def createtimetable(request,class_id=None,set_id=None):
    if request.method=='POST':
        for i in range(1,6):
            t_obj=TimetableModel()
            a='s'+str(i)
            a=request.POST[a]
            #foriegn key choices are stored as referenced objects but normal user defined choices are stored as the first element in the tuple defined
            t_obj.subject=get_object_or_404(SubjectModel,id=a)
            a=request.POST['set_name']
            t_obj.set_name=get_object_or_404(TimetablesetModel,id=a)
            t_obj.day=request.POST['day']
            t_obj.hour=i
            t_obj.save()
        check=TimetableModel.objects.filter(set_name__id=set_id)
        if len(check)>=30:
            messages.info(request,'You have filled for all the 6 days timetable')
            return redirect('timetable:showsubjects',class_id=class_id,set_id=set_id)
        c_object=get_object_or_404(ClassroomModel,id=class_id)
        t=TimetableForm(initial={'set_name':set_id},c_object=c_object)
        messages.success(request,'Your timetable entry gets stored')
        return render(request,'timetable/timetable.html',{'t':t,'c_object':c_object,'set_id':set_id})
    else:
        check=TimetableModel.objects.filter(set_name__id=set_id)
        if len(check)>=30:
            messages.info(request,'You have filled for all the 6 days timetable')
            return redirect('timetable:showsubjects',class_id=class_id,set_id=set_id)
        c_object=get_object_or_404(ClassroomModel,id=class_id)
        t=TimetableForm(initial={'set_name':set_id},c_object=c_object)
        return render(request,'timetable/timetable.html',{'t':t,'c_object':c_object,'set_id':set_id})

def createtimetableset(request,class_id):
    c_object=get_object_or_404(ClassroomModel,id=class_id)
    t_set=TimetablesetForm(request.POST or None)
    if t_set.is_valid():
        t_set=t_set.save(commit=False)
        #The object returned by the save(commit=false) is the model instance not the form instance so we are able to access classroom field which is not included in the form
        t_set.classroom=c_object
        t_set.save()
        return redirect('timetable:setchoose',class_id=class_id)
    return render(request,'timetable/timetableset.html',{'t_set':t_set,'c_object':c_object})

def setchoose(request,class_id):
    c_object=get_object_or_404(ClassroomModel,id=class_id)
    t_set_particular=TimetablesetModel.objects.filter(classroom=c_object)
    if t_set_particular:
        context={
            't_set_particular':t_set_particular,
            'c_object':c_object
        }
        return render(request,'timetable/setchoose.html',context)
    t_set=TimetablesetForm()
    return render(request,'timetable/timetableset.html',{'c_object':c_object,'t_set':t_set,'No_set':1})

def set_info(request,class_id,set_id):
    c_object=get_object_or_404(ClassroomModel,id=class_id)
    s_object=get_object_or_404(TimetablesetModel,id=set_id)
    t_set=TimetablesetForm(request.POST or None,instance=s_object)
    if t_set.is_valid():
        t_set.save()
        messages.success(request,'Changes made are saved')
    return render(request,'timetable/set_info.html',{'c_object':c_object,'s_object':s_object,'t_set':t_set})

def showsubjects(request,class_id,set_id):
    where_to_redirect=TimetableModel.objects.filter(set_name__id=set_id)
    if len(where_to_redirect)==0:
        c_object=get_object_or_404(ClassroomModel,id=class_id)
        t=TimetableForm(initial={'set_name':set_id},c_object=c_object)
        messages.error(request,'No subjects created for this timetable yet')
        return render(request,'timetable/timetable.html',{'t':t,'c_object':c_object,'set_id':set_id})

    s_object=get_object_or_404(TimetablesetModel,id=set_id)
    c_object=get_object_or_404(ClassroomModel,id=class_id)    
    #Subjects for the particular timetable
    all_subjects=[]
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    for i in range(1,7):
        setsubjects=TimetableModel.objects.filter(set_name__id=set_id,day=i).order_by('hour')
        j=1
        subject_list=[]
        if len(setsubjects)==0:
            all_subjects.append(['----','----','----','----','----'])
            continue
        #changes need to be done
        for s_in_t_object in setsubjects:
            while j<6:
                if s_in_t_object.hour==j:
                    subject_list.append(s_in_t_object)
                    j+=1
                    break
                else:
                    subject_list.append('----')
                    j+=1
        else:
            while j<6:
                subject_list.append('----')
                j+=1
        all_subjects.append(subject_list)
    all_subjects=zip(all_subjects,days)#zip function combines the two iterator and returns the combined version of the iterator
    subject_list=SubjectModel.objects.filter(classroom=c_object)
    edit_timetable=edit_timetableForm(subject_list=subject_list,initial={'set_name':s_object})
    return render(request,'timetable/showsubjects.html',{'all_subjects':all_subjects,'c_object':c_object,'s_object':s_object,'edit_timetable':edit_timetable})

def edit_subjects(request):
    if request.method=="POST":
       data=json.loads(request.body)
       data=data['subject_list']
       for i in data:
            subject_id=i[0]
            timetable_id=i[1]
            
            if subject_id=='Free':
                s_object=None
            else:
                s_object=get_object_or_404(SubjectModel,id=subject_id)#Implicitly on the left hand side code , subject_id is converted as a integer when comparing with integer values
            
            t_object=get_object_or_404(TimetableModel,id=timetable_id)
            t_object.subject=s_object
            t_object.save()
    return HttpResponse("saved")
            