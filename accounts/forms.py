from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from accounts.validators import *

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=40, help_text="Required a valid email address")
	phone = forms.CharField(max_length=12, validators=[validatePhone])
	class Meta:
		model = User
		fields = ['email', 'username','password1','password2','phone','first_name','last_name']