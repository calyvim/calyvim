from django.contrib import admin
from django.urls import path

from calyvim.views.home import IndexView
from calyvim.views.accounts import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("", IndexView.as_view(), name="index")
]
