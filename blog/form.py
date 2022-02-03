from tkinter import Widget
from django import forms
from .models import Blog, Comment

class KeywordSearchForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(KeywordSearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widget = forms.TextInput({"class":"form-control w-100","name":"comment","cols":"30","rows":"9","placeholder":"Write Comment"}) 