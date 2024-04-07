from django.dispatch import receiver
from django.db.models.signals import post_save

from calyvim.models import User, Schedule, ScheduleAvailability


@receiver(post_save, sender=User)
def create_default_availability(sender, instance, created, **kwargs):
    if created:
        schedule = Schedule.objects.create(
            user=instance, name="Working hours", timezone=instance.timezone
        )

        # Creating a default 1 week schedule availability
        ScheduleAvailability.objects.bulk_create(
            [
                ScheduleAvailability(
                    schedule=schedule,
                    start_time="9:00",
                    end_time="17:00",
                    weekday=ScheduleAvailability.Weekday.MONDAY,
                ),
                ScheduleAvailability(
                    schedule=schedule,
                    start_time="9:00",
                    end_time="17:00",
                    weekday=ScheduleAvailability.Weekday.TUESDAY,
                ),
                ScheduleAvailability(
                    schedule=schedule,
                    start_time="9:00",
                    end_time="17:00",
                    weekday=ScheduleAvailability.Weekday.WEDNESDAY,
                ),
                ScheduleAvailability(
                    schedule=schedule,
                    start_time="9:00",
                    end_time="17:00",
                    weekday=ScheduleAvailability.Weekday.THURSDAY,
                ),
                ScheduleAvailability(
                    schedule=schedule,
                    start_time="9:00",
                    end_time="17:00",
                    weekday=ScheduleAvailability.Weekday.FRIDAY,
                )
            ],
        )
