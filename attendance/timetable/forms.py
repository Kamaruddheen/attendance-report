from django import forms
from .models import TimetableModel, TimetablesetModel
from subject.models import SubjectModel


class TimetableForm(forms.ModelForm):
    s1 = forms.ModelChoiceField(queryset=None)
    s2 = forms.ModelChoiceField(queryset=None)
    s3 = forms.ModelChoiceField(queryset=None)
    s4 = forms.ModelChoiceField(queryset=None)
    s5 = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.choice = kwargs.pop('c_object', None)
        super().__init__(*args, **kwargs)
        self.fields['set_name'].widget.attrs.update(
            {'id': 'set_name', 'class': 'custom-select input_cust capitalize text-center form-control'})
        self.fields['day'].widget.attrs.update(
            {'id': 'day', 'class': 'custom-select input_cust capitalize text-center form-control'})
        self.fields['s1'] = forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom=self.choice), widget=forms.Select(
            attrs={'id': 's1', 'class': 'custom-select input_cust capitalize text-center form-control', }), empty_label='Free', required=False)
        self.fields['s2'] = forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom=self.choice), widget=forms.Select(
            attrs={'id': 's2', 'class': 'custom-select input_cust capitalize text-center form-control'}), empty_label='Free', required=False)
        self.fields['s3'] = forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom=self.choice), widget=forms.Select(
            attrs={'id': 's3', 'class': 'custom-select input_cust capitalize text-center form-control'}), empty_label='Free', required=False)
        self.fields['s4'] = forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom=self.choice), widget=forms.Select(
            attrs={'id': 's4', 'class': 'custom-select input_cust capitalize text-center form-control'}), empty_label='Free', required=False)
        self.fields['s5'] = forms.ModelChoiceField(queryset=SubjectModel.objects.filter(classroom=self.choice), widget=forms.Select(
            attrs={'id': 's5', 'class': 'custom-select input_cust capitalize text-center form-control'}), empty_label='Free', required=False)
        self.fields['s1'].label = "Hour I"
        self.fields['s2'].label = "Hour II"
        self.fields['s3'].label = "Hour III"
        self.fields['s4'].label = "Hour IV"
        self.fields['s5'].label = "Hour V"

    class Meta:
        model = TimetableModel
        fields = ('day', 'set_name')


class TimetablesetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'input_cust capitalize text-center form-control'})
        self.fields['from_date'].widget.attrs.update(
            {'type': 'date', 'class': 'input_cust upper_case text-center form-control'})
        self.fields['to_date'].widget.attrs.update(
            {'type': 'date', 'class': 'input_cust upper_case text-center form-control'})

    def clean(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if from_date > to_date:
            raise forms.ValidationError('date error')
        return self.cleaned_data

    class Meta:
        model = TimetablesetModel
        fields = ('name', 'from_date', 'to_date')


class edit_timetableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.choice = kwargs.pop('subject_list')
        super().__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(
            queryset=self.choice, empty_label='Free')
        self.fields['subject'].widget.attrs.update(
            {'class': 'custom-select input_cust capitalize text-center form-control'})

    class Meta:
        model = TimetableModel
        fields = ['set_name', 'day', 'hour', 'subject']


class choose_set_form(forms.Form):
    choose_set = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        choice = kwargs.pop('t_set_particular')
        super().__init__(*args, **kwargs)
        self.fields['choose_set'].queryset = choice
        self.fields['choose_set'].widget.attrs.update(
            {'class': 'custom-select input_cust capitalize text-center form-control'})
        self.fields['choose_set'].label = "Select Timetable set"
