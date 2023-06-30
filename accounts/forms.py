from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.forms import PasswordInput

from .models import CustomUser, EmailChangeRequest


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username"]


# class AppearanceChangeForm(forms.ModelForm):
#     background_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color', 'onchange': 'this.form.submit();'}))
#     navbar_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color', 'onchange': 'this.form.submit();'}))
#     profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'image-input', 'onchange': 'this.form.submit();'}), label=False)
#     default_image = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'default_image'}), required=False)
#
#     class Meta:
#         model = CustomUser
#         fields = ["profile_image", "background_color"]

class AppearanceChangeForm(forms.ModelForm):
    background_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'hidden-fields'}), label=False, required=False)
    avatar_choice = forms.CharField(widget=forms.HiddenInput(), required=False)
    avatar_draw = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'hidden-fields'}), label=False, required=False)

    class Meta:
        model = CustomUser
        fields = ["avatar", "background_color"]





class UsernameChangeForm(forms.ModelForm):
    current_password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username']

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("The current password is incorrect.")
        return current_password


class EmailChangeRequestForm(forms.ModelForm):
    class Meta:
        model = EmailChangeRequest
        fields = ['new_email']

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if CustomUser.objects.filter(email=new_email).exists():
            raise ValidationError("E-mail address is already in use.")
        return new_email


class EmailChangeConfirmationForm(forms.Form):
    confirmation_code = forms.UUIDField()
    current_password = forms.CharField(widget=PasswordInput())
