import httpx
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "alison or alison@gmail.com"}
        )
    )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "Password",
            }
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    recaptcha_response = forms.CharField(required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if settings.RECAPTCHA_ENABLED:
    #         # Run Recaptcha Server side validation
    #         recaptcha_response = cleaned_data.get("recaptcha_response", None)
    #         if not recaptcha_response:
    #             raise ValidationError("Re-captcha validation failed!")

    #         res = httpx.post(
    #             "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    #             data={
    #                 "secret": settings.RECAPTCH_SECRET_KEY,
    #                 "response": recaptcha_response,
    #             },
    #         )
    #         if not res.status_code == 200:
    #             raise ValidationError("Re-captcha validation failed!")


class ProfileForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
