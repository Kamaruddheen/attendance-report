from django import forms
from .models import ClassroomModel

class ClassroomForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['course'].widget.attrs.update({'class':'form-control identify','id':'course'})
        self.fields['year'].widget.attrs.update({'class':'form-control identify','id':'year'})
        self.fields['sec'].widget.attrs.update({'class':'form-control identify','id':'section'})
        self.fields['tutor'].widget.attrs.update({'class':'form-control identify','id':'tutor'})
    class Meta:
        model=ClassroomModel
        fields="__all__"