from django import forms
from .models import User

class CreateStaffForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'placeholder':'Enter Password'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(
		attrs={'placeholder':'Confirm Password'}))
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password','confirm_password']