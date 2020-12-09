from django import forms

from .models import SubjectModel
from classroom.models import ClassroomModel
from user_module.models import User

sub_types = (
    ('reg', 'Regular'), ('sel', 'Selective')
)


class CreateSubjectForm(forms.ModelForm):
    hour_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'SE, PCD, Lang, etc...', 'class': 'input_cust col-md-6'}),
        label="Hour Name")
    sub_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Full Subject Name', 'class': 'input_cust'}),
        label="Subject Name")
    sub_type = forms.ChoiceField(choices=sub_types, widget=forms.Select(
        attrs={'class': 'input_cust'}),
        label="Subject Type")
    handled_by = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'input_cust'}), queryset=User.objects.filter(user_type=2),
        label="Handled By")
    classroom = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'input_cust'}), queryset=ClassroomModel.objects.all())

    class Meta:
        model = SubjectModel
        fields = ['hour_name', 'sub_name',
                  'sub_type', 'handled_by', 'classroom']
