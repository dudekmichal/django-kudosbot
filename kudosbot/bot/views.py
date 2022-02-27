from django.shortcuts import render
from django.http import HttpResponse
from .models import Kudos
from .utils import create_bot


def index(request):
    # return HttpResponse('Hello, world!')
    return render(request, template_name="bot/info.html")


def enable(request):
    create_bot()
    context = {"last_kudos_id": Kudos.objects.latest('id').id,
               "all_kudos:": Kudos.get_all_kudos()}
    return render(request, template_name="bot/status.html", context=context)


def status(request):
    context = {"last_kudos_id": Kudos.objects.latest('id').id,
               "last_hundred_kudos": Kudos.get_last_hundred_kudos()}
    return render(request, template_name="bot/status.html", context=context)
