from django import forms
from .models import ClassroomModel

class ClassroomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update(
            {'class': 'input_cust'})
        self.fields['year'].widget.attrs.update(
            {'class': 'input_cust'})
        self.fields['sec'].widget.attrs.update(
            {'class': 'input_cust'})
        self.fields['tutor'].widget.attrs.update(
            {'class': 'input_cust'})
        self.fields['course'].label = "Name of the Course"
        self.fields['tutor'].label = "Tutor Name"
        self.fields['sec'].required = True

    class Meta:
        model = ClassroomModel
        fields = ['course', 'year', 'sec', 'tutor']
