import jwt
import uuid
import httpx
import random
from urllib.parse import urlencode
from django.utils.text import slugify
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.urls import reverse

from calyvim.forms.accounts import RegisterForm, LoginForm, ProfileForm
from calyvim.models import User, ConnectedAccount
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

            user.confirmed_at = timezone.now()
            user.save()

        except jwt.ExpiredSignatureError:
            messages.warning(request, "Your invitation link has been expired.")
            return redirect("login")

        except Exception:
            messages.error(request, "Something wen't wrong while verifying email.")
            return redirect("login")

        # Send Welcome email.

        login(request, user)
        return redirect("event-list")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")


class GoogleOAuthView(View):
    def get(self, request):
        base_url = "https://accounts.google.com/o/oauth2/v2/auth?"
        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]
        params = {
            "scope": " ".join(scopes),
            "access_type": "offline",
            "included_granted_scopes": "true",
            "response_type": "code",
            "redirect_uri": f"{settings.SITE_URL}{reverse('google-oauth-callback')}",
            "state": uuid.uuid4().hex,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        }
        redirect_url = base_url + urlencode(params)
        return redirect(redirect_url)


class GoogleOAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": f"{settings.SITE_URL}{reverse('google-oauth-callback')}",
            "grant_type": "authorization_code",
        }

        google_token_response = httpx.post(
            url="https://oauth2.googleapis.com/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        access_token = google_token_response.json().get("access_token")
        google_profile_res = httpx.get(
            url="https://www.googleapis.com/userinfo/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile = google_profile_res.json()
        user = User.objects.filter(email=profile.get("email")).first()
        if not user:
            user = User(
                username=slugify(profile.get("name")) + str(random.randint(1000, 9999)),
                email=profile.get("email"),
                full_name=profile.get("name"),
                confirmed_at=timezone.now(),
            )
        user.google_identity_uid = profile.get("id")
        user.save()
        login(request, user)
        return redirect("index")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(
            initial={
                "username": request.user.username,
                "full_name": request.user.full_name,
            }
        )
        context = {
            "form": form,
            "has_google_connected": request.user.connected_accounts.exists(),
        }
        return render(request, "accounts/profile.html", context)


class ConnectedAccountGoogle(LoginRequiredMixin, View):
    def get(self, request):
        next_path = request.GET.get("next_path", None)
        base_url = "https://accounts.google.com/o/oauth2/v2/auth?"
        params = {
            "scope": "https://www.googleapis.com/auth/calendar",
            "access_type": "offline",
            "included_granted_scopes": "true",
            "response_type": "code",
            "redirect_uri": f"{settings.SITE_URL}{reverse('connected-accounts-google-callback')}",
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        }
        if next_path:
            params["state"] = next_path
        redirect_url = base_url + urlencode(params)
        return redirect(redirect_url)


class ConnectedAccountGoogleCallback(LoginRequiredMixin, View):
    def get(self, request):
        code = request.GET.get("code")
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": f"{settings.SITE_URL}{reverse('connected-accounts-google-callback')}",
            "grant_type": "authorization_code",
        }

        google_token_response = httpx.post(
            url="https://oauth2.googleapis.com/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        print(google_token_response.json())

        data = google_token_response.json()
        connected_account = ConnectedAccount.objects.filter(
            user=request.user, service=ConnectedAccount.Service.GOOGLE
        ).first()
        if not connected_account:
            connected_account = ConnectedAccount(
                user=request.user, service=ConnectedAccount.Service.GOOGLE
            )

        connected_account.access_token = data["access_token"]
        connected_account.refresh_token = data["refresh_token"]
        connected_account.expiry_date = timezone.now() + timezone.timedelta(
            seconds=data["expires_in"]
        )
        connected_account.save()

        next_path = request.GET.get("next")
        if next_path:
            return redirect(next_path)

        return redirect("profile")


class ConnectedAccountGoogleRevoke(LoginRequiredMixin, View):
    def get(self, request):
        connected_account = ConnectedAccount.objects.filter(
            user=request.user, service=ConnectedAccount.Service.GOOGLE
        ).first()

        if not connected_account:
            raise Http404()

        res = httpx.post(
            url=f"https://oauth2.googleapis.com/revoke?token={connected_account.refresh_token}"
        )

        if not res.status_code == 200:
            raise Http404()

        connected_account.delete()

        if request.GET.get("next_path"):
            return redirect(request.GET.get("next_path"))

        return redirect("profile")