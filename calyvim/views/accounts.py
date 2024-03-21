import jwt
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import Http404
from django.utils import timezone

from calyvim.forms.accounts import RegisterForm, LoginForm
from calyvim.models.user import User
from calyvim.tasks import send_confirmation_email


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, "Please enter valid login information.")
            return redirect("login")

        data = form.cleaned_data
        if "@" in data.get("username_or_email"):
            kwargs = {"email": data.get("username_or_email")}
        else:
            kwargs = {"username": data.get("username_or_email")}

        user = User.objects.filter(**kwargs).first()

        if not user:
            messages.warning(
                request, "No account found with the given username or email."
            )
            return redirect("login")

        if not user.check_password(data.get("password")):
            messages.warning(request, "Invalid credentials entered.")
            return redirect("login")

        if not user.is_active:
            messages.error(
                request,
                "Your account has been temporarily disabled. Please contact our support team for further assistance.",
            )
            return redirect("login")

        if user.is_password_expired:
            messages.warning(
                request,
                "Please reset your password by selecting 'Forgot your password?' to log in.",
            )
            return redirect("login")

        login(request, user)
        return redirect("event-list")


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

        # Verify Recaptcha
        recaptcha_response = data.pop("recaptcha_response")
        if settings.RECAPTCHA_ENABLED:
            # Verify recaptcha
            pass

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
        user.save()
        send_confirmation_email.delay(user.email)
        messages.success(
            request, "We have sent an verification link to verify your email."
        )
        login(request, user)
        return redirect("event-list")


class EmailConfirmView(View):
    def get(self, request, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user = User.objects.filter(
                email=data.get("email"), verified_at__isnull=True
            ).first()

            if not user:
                raise Http404("Invalid email confirmation URL")

            user.verified_at = timezone.now()
            user.save()

        except jwt.ExpiredSignatureError:
            messages.warning(request, "Your invitation link has been expired.")
            return redirect("login")

        except Exception:
            messages.error(request, "Something wen't wrong while verifying email.")
            return redirect("login")

        login(request, user)
        return redirect("event-list")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")
