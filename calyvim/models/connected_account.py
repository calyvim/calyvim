import httpx
from django.db import models
from django.utils import timezone
from django.conf import settings

from calyvim.models.base import BaseUUIDTimestampModel


class ConnectedAccount(BaseUUIDTimestampModel):
    class Service(models.TextChoices):
        GOOGLE = ("google", "Google")
        MICROSOFT = ("microsoft", "Microsoft")
        ZOOM = ("zoom", "Zoom")

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="connected_accounts"
    )
    service = models.CharField(max_length=20, choices=Service.choices)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "connected_accounts"
        unique_together = ["user_id", "service"]

    def __str__(self) -> str:
        return str(self.id)

    @property
    def token(self):
        if timezone.now() > self.expiry_date:
            # The token has been expired
            # Call GoogleAPI's for new access token

            body = {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            }
            res = httpx.post(
                url="https://oauth2.googleapis.com/token",
                data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            data = res.json()

            self.access_token = data["access_token"]
            self.expiry_date = timezone.now() + timezone.timedelta(
                seconds=data["expires_in"]
            )
            self.save(update_fields=["access_token", "expiry_date"])

        return self.access_token
