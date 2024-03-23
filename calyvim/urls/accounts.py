from django.urls import path

from calyvim.views.accounts import (
    LoginView,
    RegisterView,
    ProfileView,
    LogoutView,
    EmailConfirmView,
    GoogleOAuthCallbackView,
    GoogleOAuthView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "email/confirm/<str:token>/",
        EmailConfirmView.as_view(),
        name="email-confirm",
    ),
    path("google/oauth/", GoogleOAuthView.as_view(), name="google-oauth"),
    path(
        "google/oauth/callback/",
        GoogleOAuthCallbackView.as_view(),
        name="google-oauth-callback",
    ),
]
