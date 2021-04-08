from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    username =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))