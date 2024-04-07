import pytz
from django.db import models

from calyvim.models.base import BaseUUIDTimestampModel


class Schedule(BaseUUIDTimestampModel):
    TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="schedules")
    name = models.CharField(max_length=150)
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default="UTC")

    class Meta:
        db_table = "schedules"

    def __str__(self) -> str:
        return str(self.id)


class ScheduleAvailability(BaseUUIDTimestampModel):
    class Weekday(models.IntegerChoices):
        MONDAY = (0, "Monday")
        TUESDAY = (1, "Tuesday")
        WEDNESDAY = (2, "Wednesday")
        THURSDAY = (3, "Thursday")
        FRIDAY = (4, "Friday")
        SATURDAY = (5, "Saturday")
        SUNDAY = (6, "Sunday")

    schedule = models.ForeignKey(
        "Schedule", on_delete=models.CASCADE, related_name="availabilities"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.SmallIntegerField(choices=Weekday.choices)

    class Meta:
        db_table = "schedule_availabilities"
        verbose_name = "Schedule Availability"
        verbose_name_plural = "Schedule Availabilities"

    def __str__(self) -> str:
        return str(self.id)
