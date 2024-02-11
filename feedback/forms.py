from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-comment', 'rows': 5,'placeholder':'Comment'}))
    class Meta:
        model = Comment
        fields = ['text']


