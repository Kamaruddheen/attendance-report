from django.http import QueryDict
from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render,get_object_or_404
from .forms import TimetableForm,TimetablesetForm,Timetablesetchoose,CreatetimetableForm
from .models import ClassroomModel,TimetableModel,TimetablesetModel,SubjectModel
# Create your views here.
def createtimetable(request,id=None):
    c_object=get_object_or_404(ClassroomModel,id=id)
    t=TimetableForm(request.POST or None,id=id)
    return render(request,'timetable/timetable.html',{'t':t,'c_object':c_object})

def createtimetableset(request,id):
    c_object=get_object_or_404(ClassroomModel,id=id)
    t_set=TimetablesetForm(request.POST or None)
    if t_set.is_valid():
        t_set=t_set.save(commit=False)
        #The object returned by the save(commit=false) is the model instance not the form instance so we are able to access classroom field which is not included in the form
        t_set.classroom=c_object
        t_set.save()
        return redirect('timetable:createtimetable',id=id)
    return render(request,'timetable/timetableset.html',{'t_set':t_set,'c_object':c_object})
   
def setchoose(request,id):
    c_object=get_object_or_404(ClassroomModel,id=id)
    t_set_particular=TimetablesetModel.objects.filter(classroom=c_object)
    if t_set_particular:
        t_set_choose=Timetablesetchoose(c_object=c_object)
        context={
            't_set_choose':t_set_choose,
            'c_object':c_object
        }
        return render(request,'timetable/setchoose.html',context)
    return redirect('timetable:createtimetableset',id=id)

def showsubjects(request,id):
    set_id=request.POST.get('setchoose')#set id for the form
    set_object=get_object_or_404(TimetablesetModel,id=set_id)
    #classroom subjects
    s_list=SubjectModel.objects.filter(classroom__id=id)
    #sent to form to choose the list of choices to be shown
    t_form_object=CreatetimetableForm(initial={'set_name':set_id},s_list=s_list)#This is the place where form object is created
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
    
    return render(request,'timetable/showsubjects.html',{'set_id':set_id,'t_form_object':t_form_object,'days':days,'all_subjects':all_subjects})
