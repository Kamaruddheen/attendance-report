from django import forms
from .models import TimetableModel
from subject.models import SubjectModel


class TimetableForm(forms.ModelForm):
    s1=forms.ModelChoiceField(queryset=None)
    s2=forms.ModelChoiceField(queryset=None)
    s3=forms.ModelChoiceField(queryset=None)
    s4=forms.ModelChoiceField(queryset=None)
    s5=forms.ModelChoiceField(queryset=None)
    def __init__(self,*args,**kwargs):
        self.choice=kwargs.pop('id',None)
        super().__init__(*args,**kwargs)
        self.fields['set_name'].widget.attrs.update({'id':'set_name','class':'form-control'})
        self.fields['day'].widget.attrs.update({'id':'day','class':'form-control'})
        self.fields['s1']=forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom__id=self.choice),widget=forms.Select(attrs={'id':'s1','class':'form-control'}))
        self.fields['s2']=forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom__id=self.choice),widget=forms.Select(attrs={'id':'s2','class':'form-control'}))
        self.fields['s3']=forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom__id=self.choice),widget=forms.Select(attrs={'id':'s3','class':'form-control'}))
        self.fields['s4']=forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom__id=self.choice),widget=forms.Select(attrs={'id':'s4','class':'form-control'}))
        self.fields['s5']=forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom__id=self.choice),widget=forms.Select(attrs={'id':'s5','class':'form-control'}))
    class Meta:
        model=TimetableModel
        fields=('day','set_name')

