from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class signup(UserCreationForm,forms.Form):
    class meta:
        model = User
        fields = '__all__'


class profile_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = '__all__'
        exclude = ['joined_at','user']


class user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']