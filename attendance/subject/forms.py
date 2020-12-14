from django import forms

from .models import SubjectModel
from classroom.models import ClassroomModel


class CreateSubjectForm(forms.ModelForm):

    class Meta:
        model = SubjectModel
        fields = ['hour_name', 'sub_name',
                  'sub_type', 'handled_by', 'classroom']

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff')
        if staff.is_hod:
            queryset = ClassroomModel.objects.all()
        else:
            queryset = ClassroomModel.objects.filter(tutor_id=staff.user.id)
        super(CreateSubjectForm, self).__init__(*args, **kwargs)
        self.fields['classroom'].queryset = queryset
        self.fields['hour_name'].widget.attrs.update(
            {'class': 'input_cust  col-md-6', 'placeholder': 'SE, PCD, Lang, Elective etc...'})
        self.fields['sub_name'].widget.attrs.update(
            {'class': 'input_cust', 'placeholder': 'Full Subject Name'})
        self.fields['sub_type'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['handled_by'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['classroom'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['hour_name'].label = "Hour Name"
        self.fields['sub_name'].label = "Subject Name"
        self.fields['sub_type'].label = "Subject Type"
        self.fields['handled_by'].label = "Handled By"
