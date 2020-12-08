from django import forms
from .models import ClassroomModel

class ClassroomForm(forms.ModelForm):
    id=forms.CharField(max_length=10,required=False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['id'].widget.attrs.update({'class':'form-control','id':'id','readonly':True})
        self.fields['course'].widget.attrs.update({'class':'form-control identify','id':'course'})
        self.fields['year'].widget.attrs.update({'class':'form-control identify'})
        self.fields['sec'].widget.attrs.update({'class':'form-control identify','id':'section'})
        self.fields['tutor'].widget.attrs.update({'class':'form-control identify','id':'tutor'})
    class Meta:
        model=ClassroomModel
        fields="__all__"


