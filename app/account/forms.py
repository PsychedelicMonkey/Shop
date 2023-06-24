from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class EditProfileForm(forms.ModelForm):
    is_private = forms.BooleanField(required=False, label='Private', help_text='If your account is set to private, '
                                                                               'your name will not appear on product '
                                                                               'reviews')

    class Meta:
        model = Profile
        fields = ('image', 'bio', 'is_private',)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
