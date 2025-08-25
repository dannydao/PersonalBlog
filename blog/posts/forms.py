from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["cover","cover_url","title", "body"]
        widgets = {
            "cover": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]