from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'favorite_tracks',)
        widgets = {
            'favorite_tracks': forms.CheckboxSelectMultiple(),
        }
