from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404
from django.utils import timezone

from calyvim.models import Event, User


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/index.html")
    

class OverviewView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/overview.html")


class CalenderBookingView(View):
    def get(self, request, username, slug):
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404

        event = Event.objects.filter(slug=slug, user=user).first()
        if not event:
            raise Http404

        schedule = event.schedule
        schedule_availabilities = schedule.availabilities.all()

        today = timezone.now() - timezone.timedelta(days=15)
        print(today)
        print(today.weekday())
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_weekday = start_of_month.weekday()
        # print(start_weekday.weekday())
        # print(today.month)
        # print(today.date())
        # print(today.weekday())

        days = []
        week = []
        for i in range(1, 32):
            if i % 7 != 0:
                week.append(i)
            else:
                week.append(i)
                days.append(week)
                week = []
        days.append(week)
        
        print(days)

        context = {
            "user": user,
            "event": event,
            "days": days
        }
        return render(request, "home/calender_booking.html", context)
