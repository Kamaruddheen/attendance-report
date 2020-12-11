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
    #classroom subjects
    s_list=SubjectModel.objects.filter(classroom__id=id)
    #sent to form to choose the list of choices to be shown
    s_object=CreatetimetableForm(request.POST or None,s_list=s_list)#This is the place where form object is created
    #Subjects for the particular timetable
    setsubjects=TimetableModel.objects.filter(set_name__id=set_id)#subjects to be displayed as a timetable view in te form
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    return render(request,'timetable/showsubjects.html',{'set_id':set_id,'set_object':s_object,'days':days,'setsubjects':setsubjects})
