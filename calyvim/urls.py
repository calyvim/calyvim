from django.contrib import admin
from django.urls import path

from calyvim.views.home import IndexView
from calyvim.views.accounts import LoginView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("", IndexView.as_view(), name="index")
]
