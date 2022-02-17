from tkinter import Widget
from django import forms
from .models import Blog, Comment

class TitleSearchForm(forms.Form):
    title = forms.CharField(required=True)
    # class Meta:
    #     model = Blog
    #     fields = ['title']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widget = forms.TextInput({"class":"form-control w-100","name":"comment","cols":"30","rows":"9","placeholder":"Write Comment"}) 