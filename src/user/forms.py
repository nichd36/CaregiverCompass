from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from captcha.widgets import ReCaptchaV2Checkbox


from user.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Please enter email')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

# class PasswordUpdateForm(forms.ModelForm):
#     oldpassword = forms.CharField(label='Old password', widget=forms.PasswordInput)
#     password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

#     class Meta:
#         model = Account
#         fields = ('email', 'password')

#     def clean(self):
#         if self.is_valid():
#             email = self.cleaned_data['email']
#             password = self.cleaned_data['password']

#             if not authenticate(email=email, password=password):
#                 raise forms.ValidationError("Invalid Login")
            
class AccountUpdateForm(forms.ModelForm):
    remove_profile_pic = forms.BooleanField(required=False)  # Add a new field to the form

    class Meta:
        model = Account
        fields = ('image','email', 'username')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = CustomClearableFileInput()
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account.email)
        
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % account.username)
    # image = forms.ImageField(label="image", required=False)
    def clean(self):
        cleaned_data = super().clean()
        remove_profile_pic = cleaned_data.get('remove_profile_pic', False)

        if remove_profile_pic:
            cleaned_data['image'] = None

        return cleaned_data
from django.forms.widgets import ClearableFileInput

class SocialAccountUpdateForm(forms.ModelForm):
    remove_profile_pic = forms.BooleanField(required=False)  # Add a new field to the form

    class Meta:
        model = Account
        fields = ('image', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = CustomClearableFileInput()
        
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % account.username)

    def clean(self):
        cleaned_data = super().clean()
        remove_profile_pic = cleaned_data.get('remove_profile_pic', False)

        if remove_profile_pic:
            cleaned_data['image'] = None

        return cleaned_data
    
from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, None, attrs=attrs, renderer=renderer)

