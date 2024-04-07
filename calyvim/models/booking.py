from django.db import models

from calyvim.models.base import BaseUUIDTimestampModel


class Booking(BaseUUIDTimestampModel):
    class Status(models.TextChoices):
        CANCELLED = ("cancelled", "Cancelled")
        ACCEPTED = ("accepted", "Accepted")
        REJECTED = ("rejected", "Rejected")
        PENDING = ("pending", "Pending")

    event = models.ForeignKey("Event", on_delet=models.CASCADE, related_name="bookings")
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = "bookings"

    def __str__(self) -> str:
        return str(self.id)
