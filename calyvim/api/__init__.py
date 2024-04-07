from django.urls import path

from calyvim.api.accounts import LoginAPIView, UsernameCheckAPIView, RegisterView

# fmt: off
urlpatterns = [
    path("accounts/login/", LoginAPIView.as_view(), name="accounts-login-api"),
    path("accounts/register/", RegisterView.as_view(), name="accounts-register-api"),
    path("accounts/username-check/", UsernameCheckAPIView.as_view(), name="accounts-username-check-api"),
]
