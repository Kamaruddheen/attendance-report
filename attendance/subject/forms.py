from django import forms
from django.shortcuts import get_object_or_404

from .models import SubjectModel
from classroom.models import ClassroomModel
from user_module.models import User

sub_types = (
    ('reg', 'Regular'), ('sel', 'Selective')
)


class CreateSubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff')
        if staff.is_hod:
            queryset = ClassroomModel.objects.all()
        else:
            queryset = ClassroomModel.objects.filter(tutor_id=staff.user.id)
        super(CreateSubjectForm, self).__init__(*args, **kwargs)
        self.fields['classroom'].queryset = queryset

    hour_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'SE, PCD, Lang, Elective etc...', 'class': 'input_cust col-md-6'}),
        label="Hour Name")
    sub_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Full Subject Name', 'class': 'input_cust'}),
        label="Subject Name")
    sub_type = forms.ChoiceField(choices=sub_types, widget=forms.Select(
        attrs={'class': 'input_cust capitalize'}),
        label="Subject Type")
    handled_by = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'input_cust capitalize'}), queryset=User.objects.filter(user_type=2),
        label="Handled By")
    classroom = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'input_cust capitalize'}), queryset=ClassroomModel.objects.none())

    class Meta:
        model = SubjectModel
        fields = ['hour_name', 'sub_name',
                  'sub_type', 'handled_by', 'classroom']
