from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class UserVerificationWarningMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.verified_at is None:
            messages.warning(request, "Please verify your email address.")
        return super().dispatch(request, *args, **kwargs)
