from django import forms
from .models import ClassroomModel

from user_module.models import User


class ClassroomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update(
            {'class': 'input_cust', 'placeholder': 'eg..BSC Computer Science,...'})
        self.fields['year'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['sec'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['tutor'].widget.attrs.update(
            {'class': 'input_cust capitalize'})
        self.fields['course'].label = "Name of the Course"
        self.fields['tutor'].label = "Tutor Name"
        self.fields['sec'].required = True

    class Meta:
        model = ClassroomModel
        fields = ['course', 'year', 'sec', 'tutor']


class AddStudentCSVForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'custom-file-input'}))


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username', 'class': 'input_cust capitalize'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First name', 'class': 'input_cust capitalize'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last name', 'class': 'input_cust capitalize'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'eg..abc@example.com', 'class': 'input_cust'})
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email Address"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class BaseStudentFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseStudentFormSet,self).__init__(*args, **kwargs)
        self.queryset = User.objects.none()
        for form in self.forms:
            form.empty_permitted=False

    def clean(self):
        if any(self.errors):
            return
        usernames = []
        emails = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if username in usernames:
                raise ValidationError(
                    "Students in the set must have distinct username")
            usernames.append(username)
            if email in emails:
                raise ValidationError(
                    "Students in the set must have distinct email")
            emails.append(email)
