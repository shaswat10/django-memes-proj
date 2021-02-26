from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.utils.translation import gettext_lazy as _
###########

class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(error_messages={
               'required': 'Enter the password field'
                },
        label = "Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    password2 = forms.CharField(error_messages={
               'required': 'Enter the confirm password field'
                },
    label = "Confirm Password",
    widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email',]

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'required':'true', 'type':'email'}),
            # 'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'username': {
                'required': _("Username is required!"),
            },
            'email':{'required': _("Email field is required!")}
        }

