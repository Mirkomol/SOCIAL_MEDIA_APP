from django import forms
from .models import PostComment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget = forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Comment Here...',
        'rows':'4',

    }))

    class Meta:
        model = PostComment
        fields = ('content',)

