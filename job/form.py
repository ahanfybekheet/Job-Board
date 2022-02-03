from django import forms
from .models import *

class apply(forms.ModelForm,forms.Form):
    class Meta:
        model = apply_job
        fields = [
            'name',
            'email',
            'website',
            'cv',
            'coverletter', 
         ]
        widgets = {
            'name' : forms.TextInput(attrs={'type':"text" ,'placeholder':"Your name"}),
            'email': forms.EmailInput(attrs={'type':"text" ,'placeholder':"Email"}),
            'website' : forms.URLInput(attrs={'type':"text" ,'placeholder':"Website/Portfolio link"}),
            'coverletter': forms.Textarea(attrs={"name":"#",' id':"" ,"cols":"30" ,"rows":"10" ,"placeholder":"Coverletter"})
        }








class job_post_form(forms.ModelForm):
    class Meta:
        model = job
        fields = '__all__'
        exclude = ('slug','user','publish_at')


class filter(forms.ModelForm,forms.Form):
    def __init__(self, *args, **kwargs):
        super(filter, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['experince'].required = False
        self.fields['job_type'].required = False
        self.fields['categorie'].required = False
        self.fields['salary'].required = False

    class Meta:
        model = job
        fields = ['title','experince','categorie','salary','job_type']
        widgets ={
            'title'     : forms.TextInput({'type':"text", "placeholder":"Title"}),
            'experince' : forms.TextInput({'type':"text", "placeholder":"Experince"}),
            'job_type'  : forms.Select(attrs={'class':'wide','placeholder':'Job Type'}),
            'categorie' : forms.Select(attrs={'class':'wide'}),
            'salary'    : forms.TextInput(attrs={'class':'wide','placeholder':'salary'})
        }
