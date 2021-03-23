from django import forms

from .models import SubjectModel, HourModel
from classroom.models import ClassroomModel


class CreateSubjectForm(forms.ModelForm):

    class Meta:
        model = SubjectModel
        fields = ['sub_name','handled_by']

    def __init__(self, *args, **kwargs):
        # staff = kwargs.pop('staff')
        # if staff.is_hod:
        #     queryset = ClassroomModel.objects.all()
        # else:
        #     queryset = ClassroomModel.objects.filter(tutor_id=staff.user.id)
        super(CreateSubjectForm, self).__init__(*args, **kwargs)
        # self.fields['classroom'].queryset = queryset
        # self.fields['hour_name'].widget.attrs.update(
        #     {'class': 'input_cust  col-md-6', 'placeholder': 'SE, PCD, Lang, Elective etc...'})
        self.fields['sub_name'].widget.attrs.update(
            {'class': 'input_cust', 'placeholder': 'Full Subject Name'})
        # self.fields['sub_type'].widget.attrs.update(
        #     {'class': 'input_cust capitalize'})
        self.fields['handled_by'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        # self.fields['classroom'].widget.attrs.update(
        #     {'class': 'input_cust capitalize'})
        # self.fields['hour_name'].label = "Hour Name"
        self.fields['sub_name'].label = "Subject Name"
        # self.fields['sub_type'].label = "Subject Type"
        self.fields['handled_by'].label = "Handled By"

class CreateHourForm(forms.ModelForm):

    class Meta:
        model = HourModel
        fields = ['name','hour_type']

class HourFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(HourFormSet,self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted=False

    # def clean(self):
    #     if any(self.errors):
    #         return
    #     usernames = []
    #     emails = []
    #     for form in self.forms:
    #         if self.can_delete and self._should_delete_form(form):
    #             continue
    #         username = form.cleaned_data.get('username')
    #         email = form.cleaned_data.get('email')
    #         if username in usernames:
    #             raise ValidationError(
    #                 "Students in the set must have distinct username")
    #         usernames.append(username)
    #         if email in emails:
    #             raise ValidationError(
    #                 "Students in the set must have distinct email")
    #         emails.append(email)


class SubjectAddStudentsForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        request = kwargs.pop('request',None)
        sub_list = kwargs.pop('sub_list',None)
        super().__init__(*args,**kwargs)
        sub_obj = self.instance
        other_students = sub_obj.students.none()
        for i in sub_list:
            if not i.id == sub_obj.id:
                other_students = other_students.union(i.students.all())
        class_students = sub_obj.hour.classroom.students.all().exclude(pk__in=[i.id for i in other_students])
        self.fields['students'] = forms.ModelMultipleChoiceField(queryset=class_students,widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = SubjectModel
        fields = ['students']