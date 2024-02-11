from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'signup-form__input','placeholder':'Name','required':'required'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'signup-form__input','placeholder':'Email','required':'required'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'signup-form__input','placeholder':'First Name','required':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'signup-form__input','placeholder':'Last Name','required':'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signup-form__input','placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signup-form__input','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email','password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match'
            )


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'id':'profile-picture-img','class':'input-img'}), validators= [allow_only_images_validator],required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...','required':'required','class':'custom-input'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Country','class':'custom-input'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State','class':'custom-input'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City','class':'custom-input'}))
    pin_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Pin Code','class':'custom-input'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Latitude','class':'custom-input latitude_class'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Longitude','class':'custom-input longitude_class'}))
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'input-img', 'id':'cover-picture-img'}), validators=[allow_only_images_validator],required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']

class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name','class':'custom-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'custom-input'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone Number','class':'custom-input'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']