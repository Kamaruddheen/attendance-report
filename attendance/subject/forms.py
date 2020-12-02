from django import forms

from .models import SubjectModel

class CreateSubjectForm(forms.ModelForm):
	class Meta:
		model = SubjectModel
		fields = ['hour_name','sub_name','sub_type','handled_by','classroom']