from django import forms
from .models import User


class CreateStaffForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'input_cust border_white'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username', 'class': 'input_cust capitalize', 'autocomplete': 'new-password'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First name', 'class': 'input_cust capitalize'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last name', 'class': 'input_cust capitalize'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'eg..abc@example.com', 'class': 'input_cust'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Enter Password', 'class': 'input_cust'})
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email Address"

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email

    def clean_confirm_password(self):
        c_pass = self.cleaned_data.get('confirm_password')
        if not c_pass == self.cleaned_data.get('password'):
            raise forms.ValidationError('Password did not match')
        return c_pass


class EditStaffForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

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

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email
