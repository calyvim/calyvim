from django.views import View
from django.shortcuts import render

from calyvim.forms.accounts import RegisterForm


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})
