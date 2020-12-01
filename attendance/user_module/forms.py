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
		fields = ['username','first_name','last_name','email',]

	def clean_email(self):
		email = self.cleaned_data.get('email').lower()
		return email