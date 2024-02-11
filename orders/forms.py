from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # country = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    # state = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    # city = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    # pin_code = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address','country','state','city','pin_code']