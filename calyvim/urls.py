from django.contrib import admin
from django.urls import path, include

from calyvim.views.accounts import (
    LoginView,
    RegisterView,
    ProfileView,
    LogoutView,
    EmailConfirmView,
    GoogleOAuthCallbackView,
    GoogleOAuthView,
    ConnectedAccountGoogle,
    ConnectedAccountGoogleCallback,
    ConnectedAccountGoogleRevoke,
    ConnectedAccountsView
)
from calyvim.views.events import EventListView, EventCreateView
from calyvim.views.home import IndexView, CalenderBookingView, OverviewView

# fmt: off
urlpatterns = [
    path("api/", include("calyvim.api")),
    path("admin/", admin.site.urls),
    
    # Accounts routes
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/email/confirm/<str:token>/", EmailConfirmView.as_view(), name="email-confirm"),
    path("accounts/google/oauth/", GoogleOAuthView.as_view(), name="google-oauth"),
    path("accounts/google/oauth/callback/", GoogleOAuthCallbackView.as_view(), name="google-oauth-callback"),
    path("accounts/connected-accounts/", ConnectedAccountsView.as_view(), name="connected-accounts"),
    path("accounts/connected-accounts/google/", ConnectedAccountGoogle.as_view(), name="connected-accounts-google"),
    path("accounts/connected-accounts/google/callback/", ConnectedAccountGoogleCallback.as_view(), name="connected-accounts-google-callback"),
    path("accounts/connected-accounts/google/revoke/", ConnectedAccountGoogleRevoke.as_view(), name="connected-accounts-google-revoke"),
    
    # Events
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/create/", EventCreateView.as_view(), name="event-create"),
    
    # Home routes
    path("u/<str:username>/<str:slug>/", CalenderBookingView.as_view(), name="calender-booking"),
    path("overview/", OverviewView.as_view(), name="overview"),
    path("", IndexView.as_view(), name="index"),
]
