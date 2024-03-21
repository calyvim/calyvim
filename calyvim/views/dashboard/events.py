from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from calyvim.mixins import UserVerificationRequiredMixin


class EventListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/events/list.html")


class EventCreateView(LoginRequiredMixin, UserVerificationRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/events/create.html")
