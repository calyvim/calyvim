from django.contrib import messages
from django.shortcuts import redirect


class UserVerificationRequiredMixin:
     def dispatch(self, request, *args, **kwargs):
        if request.user.confirmed_at is None:
            messages.warning(request, "Please confirm your account to continue using all the services.")
            return redirect("event-list-create")
        return super().dispatch(request, *args, **kwargs)