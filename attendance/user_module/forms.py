from django import forms
from .models import User


class CreateStaffForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'input_cust'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'input_cust'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'input_cust'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'abc@example.com', 'class': 'input_cust'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'input_cust'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'input_cust border_white'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['first_name'].required = False
        self.fields['email'].required = False
        self.fields['last_name'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email

    def clean_confirm_password(self):
        c_pass = self.cleaned_data.get('confirm_password')
        if not c_pass == self.cleaned_data.get('password'):
            raise forms.ValidationError('Password did not match')
        return c_pass


class EditStaffForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'input_cust'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'input_cust'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'input_cust'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'abc@example.com', 'class': 'input_cust'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['first_name'].required = False
        self.fields['email'].required = False
        self.fields['last_name'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email
