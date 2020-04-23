from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import EventType


def index(request):
    context = {}
    return render(request, 'dashboard/base.html', context)


class EventTypeCreate(CreateView):
    model = EventType
    fields = ['name']
    template_name = 'dashboard/event_type/event_add.html'
