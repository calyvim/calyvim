from django import forms

from calyvim.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "password"})
    )


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    timezone = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        choices=User.TIMEZONE_CHOICES,
        initial="UTC",
    )
