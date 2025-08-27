from django import forms
from .models import Post, Comment, Profile

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
        labels = {"body": ""}
        widgets = {
            "body":forms.Textarea(
                attrs={
                    "placeholder": "Write a comment...",
                    "rows": 6,
                    "class": "comment-box"
                }
            )
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "bio": forms.TextInput(attrs={"placeholder": "Short bio (optional)"})
        }