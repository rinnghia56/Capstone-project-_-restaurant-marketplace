from django import forms
from accounts.validators import allow_only_images_validator
from .models import Post


class PostForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-add-img'}), validators=[allow_only_images_validator])

    class Meta:
        model = Post
        fields = ['category','post_title','content','image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-add-input'}),
            'post_title': forms.TextInput(attrs={'class': 'form-add-input'}),
            'content': forms.Textarea(attrs={'class': 'form-add-input'}),
        }
