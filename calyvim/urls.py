from django.contrib import admin
from django.urls import path

from calyvim.views.home import IndexView
from calyvim.views.accounts import (
    LoginView,
    RegisterView,
    ProfileView,
    EmailConfirmView,
)
from calyvim.views.dashboard.events import EventListView, EventCreateView

admin_urls = [
    path("admin/", admin.site.urls),
]

account_urls = [
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path(
        "accounts/email/confirm/<str:token>/",
        EmailConfirmView.as_view(),
        name="email-confirm",
    ),
]

dashboard_urls = [
    path("dashboard/events/", EventListView.as_view(), name="event-list"),
    path("dashboard/events/create/", EventCreateView.as_view(), name="event-create")
]

home_urls = [
    path("", IndexView.as_view(), name="index"),
]

urlpatterns = admin_urls + account_urls + dashboard_urls + home_urls
