from pkgutil import extend_path
import re


from django import forms 


class ContactForm(forms.Form):
    message = forms.CharField(max_length=3000,widget=forms.TextInput(),required=True)
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=False)

