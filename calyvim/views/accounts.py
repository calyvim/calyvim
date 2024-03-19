from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from calyvim.forms.accounts import RegisterForm
from calyvim.models.user import User
from calyvim.mixins import UserVerificationWarningMixin


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(
            request,
            "accounts/register.html",
            {
                "form": form,
                "recaptcha_enabled": settings.RECAPTCHA_ENABLED,
                "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
            },
        )

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if not form.is_valid():
            messages.warning(request, "Please enter valid information.")
            return redirect("register")

        data = form.cleaned_data
        existing_user = User.objects.filter(
            Q(username=data.get("username")) | Q(email=data.get("email"))
        ).first()
        if existing_user:
            messages.warning(
                request, "A user already exists with the given username or email."
            )
            return redirect("register")

        password = data.pop("password")
        user = User(**data)
        user.set_password(password)

        messages.success(
            request, "We have sent an verification link to verify your email."
        )
        return redirect("login")


class ProfileView(LoginRequiredMixin, UserVerificationWarningMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")
