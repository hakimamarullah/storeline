from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.contrib.auth import authenticate
from accounts.validators import *
from accounts.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=40, help_text="Required a valid email address")
    phone = forms.CharField(max_length=12, validators=[validatePhone])

    class Meta:
        model = User
        fields = ['email', 'username', 'password1',
                  'password2', 'phone', 'first_name', 'last_name']


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("email or password is invalid")
