from django import forms
from .models import Vendor, OpeningHour
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'id':'file__input','class':'input-img'}), validators= [allow_only_images_validator])
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={'class':'signup-form__input custom-input','placeholder':'Restaurant Name'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day','from_hour','to_hour','is_closed']