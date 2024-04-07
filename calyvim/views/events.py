from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import Http404

from calyvim.mixins.permission import UserVerificationRequiredMixin
from calyvim.forms.events import EventCreateForm, OneOnOneEventCreateForm
from calyvim.models import Event, Schedule


class EventListView(LoginRequiredMixin, View):
    def get(self, request):
        context = {"current_page": "events"}
        return render(request, "events/list.html", context)


class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        event_type = request.GET.get("event_type", Event.EventType.ONE_ON_ONE)

        match event_type:
            case Event.EventType.ONE_ON_ONE:
                form = OneOnOneEventCreateForm()
            case _:
                form = EventCreateForm()

        context = {
            "form": form,
            "schedules": request.user.schedules.all(),
            "event_type": event_type,
            "site_url": settings.SITE_URL,
        }
        return render(request, "events/create.html", context)

    def post(self, request):
        form = OneOnOneEventCreateForm(data=request.POST)
        event_type = Event.EventType(request.GET.get("event_type"))

        if not form.is_valid():
            print(form.errors)
            messages.warning(request, "Please enter valid event create details.")
            return redirect("event-create")

        data = form.cleaned_data
        schedule_id = data.pop("schedule")
        schedule = Schedule.objects.filter(user=request.user, id=schedule_id).first()
        if not schedule:
            raise Http404

        event = Event(**data, schedule=schedule, event_type=event_type)
        event.user = request.user
        event.save()
        
        return redirect("event-create")
