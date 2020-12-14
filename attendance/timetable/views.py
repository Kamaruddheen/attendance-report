from django.http import QueryDict
from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render,get_object_or_404
from .forms import TimetableForm,TimetablesetForm,CreatetimetableForm
from .models import ClassroomModel,TimetableModel,TimetablesetModel,SubjectModel
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
    return redirect('timetable:createtimetableset',class_id=class_id)

def set_info(request,class_id=None,set_id=None):
    c_object=get_object_or_404(ClassroomModel,id=class_id)
    s_object=get_object_or_404(TimetablesetModel,id=set_id)
    return render(request,'timetable/set_info.html',{'c_object':c_object,'s_object':s_object})

def showsubjects(request,class_id=None,set_id=None):
    where_to_redirect=TimetableModel.objects.filter(set_name__id=set_id)
    if len(where_to_redirect)==0:
        return redirect('timetable:createtimetable',class_id=class_id,set_id=set_id)

    s_object=get_object_or_404(TimetablesetModel,id=set_id)
    c_object=get_object_or_404(ClassroomModel,id=class_id)    
    #Subjects for the particular timetable
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    all_subjects=[]
    for i in range(1,7):
        setsubjects=TimetableModel.objects.filter(set_name__id=set_id,day=i).order_by('hour')
        j=1
        subject_list=[]
        if len(setsubjects)==0:
            all_subjects.append(['Free','Free','Free','Free','Free'])
            continue
        for s_in_t_object in setsubjects:
            while j<6:
                if s_in_t_object.hour==j:
                    subject_list.append(s_in_t_object)
                    j+=1
                    break
                else:
                    subject_list.append('Free')
                    j+=1
        else:
            while j<6:
                subject_list.append('Free')
                j+=1
        all_subjects.append(subject_list)
    all_subjects=zip(all_subjects,days)
    
    return render(request,'timetable/showsubjects.html',{'days':days,'all_subjects':all_subjects,'c_object':c_object,'s_object':s_object})