from django.contrib import admin
from django.urls import path

from calyvim.views.home import IndexView
from calyvim.views.accounts import (
    LoginView,
    RegisterView,
    ProfileView,
    EmailConfirmView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path(
        "accounts/email/confirm/<str:token>/",
        EmailConfirmView.as_view(),
        name="email-confirm",
    ),
    path("", IndexView.as_view(), name="index"),
]
