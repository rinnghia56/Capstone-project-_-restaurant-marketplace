from django import forms

from accounts.validators import allow_only_images_validator
from .models import Category, FoodItem, FoodImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        widgets = { 
            'category_name': forms.TextInput(attrs={'class': 'form-add-input','placeholder':'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-add-input','rows': '5'}),
        }



class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-add-img'}), validators=[allow_only_images_validator])

    class Meta:
        model = FoodItem
        fields = ['category','category_default', 'food_title','notice','ingredients', 'description', 'price', 'image', 'is_available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-add-input'}),
            'category_default': forms.Select(attrs={'class': 'form-add-input'}),
            'food_title': forms.TextInput(attrs={'class': 'form-add-input'}),
            'notice': forms.TextInput(attrs={'class': 'form-add-input'}),
            'ingredients': forms.TextInput(attrs={'class': 'form-add-input'}),
            'price': forms.TextInput(attrs={'class': 'form-add-input'}),
            'description': forms.Textarea(attrs={'class': 'form-add-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'toggle__input','id': 'toggle__input'}),
        }



class FoodImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-add-img'}), validators=[allow_only_images_validator])
    class Meta:
        model = FoodImage
        fields = ['image']

