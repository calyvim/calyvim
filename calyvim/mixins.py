from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class UserVerificationRequiredMixin:
     def dispatch(self, request, *args, **kwargs):
        if request.user.verified_at is None:
            messages.warning(request, "Please confirm your account to continue using all the services.")
            return redirect("event-list")
        return super().dispatch(request, *args, **kwargs)