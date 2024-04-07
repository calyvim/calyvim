from django.db import models
from django.utils.text import slugify

from calyvim.models.base import BaseUUIDTimestampModel


class Event(BaseUUIDTimestampModel):
    class EventType(models.TextChoices):
        ONE_ON_ONE = ("one_on_one", "One-on-One")
        GROUP = ("group", "Group")
        COLLECTIVE = ("collective", "Collective")
        GATHERING = ("gathering", "Gathering")

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="events")
    schedule = models.ForeignKey(
        "Schedule", on_delete=models.CASCADE, related_name="schedule_events"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, max_length=150)
    is_active = models.BooleanField(
        verbose_name="active status", default=False, db_index=True
    )
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=30, help_text="duration in minutes.")
    event_type = models.CharField(
        verbose_name="event type",
        max_length=20,
        choices=EventType.choices,
        help_text="""
            ONE_ON_ONE - One host with one invitee
            GROUP - One host with group of invitees
            COLLECTIVE - More than one host with one invitee
            GATHERING - Multiple host with multiple invitees
        """,
    )

    class Meta:
        db_table = "events"
        constraints = [
            models.UniqueConstraint(fields=["user_id", "slug"], name="unique_user_slug")
        ]

    def __str__(self) -> str:
        return self.slug

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.slug:
                self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class EventHost(BaseUUIDTimestampModel):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="hosts")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="event_hosts"
    )
    is_confirmed = models.BooleanField(
        verbose_name="confirmed attendance", default=False
    )

    class Meta:
        db_table = "event_hosts"
        constraints = [
            models.UniqueConstraint(
                fields=["event_id", "user_id"], name="unqiue_event_user"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
