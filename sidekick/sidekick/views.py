# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from roster.models import Trophies
from homebase.models import Employees
from shifts.models import Shifts
import datetime
import pytz


# @login_required # UNCOMMENT THIS BEFORE GOING LIVE
def load_page(request, template, context):

    request = get_current_user(request)

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return HttpResponse("403 unauthorized user!")

    tz = pytz.timezone("America/Los_Angeles")
    now = tz.localize(datetime.datetime.now())
    curr_user = Employees.objects.get(netid__iexact=str(request.user))
    context['user_name'] = curr_user.full_name
    context['user_img'] = "employees/"+str(curr_user.netid)+".gif"
    context['user_netid'] = str(curr_user.netid)
    context['curr_mod'] = list(Shifts.objects.filter(location='md', shift_start__lte=now, shift_end__gt=now))[0]
    context['next_mod'] = Shifts.objects.filter(location='md', shift_start__gt=now).order_by('shift_start').first()
    context['my_shift'] = Shifts.objects.filter(owner=curr_user, shift_end__gte=now).order_by('shift_start').first()
    context['my_shift_happening'] = tz.localize(context['my_shift'].shift_start) < now

    context['trophy_list'] = Trophies.objects.filter(recipient=curr_user)

    return render(request, template, context)


def get_current_user(request):
    live = False
    if not live:
        request.user = "nchera13"

    return request


def authorize(request):
    uname = str(request.user)
    return Employees.objects.filter(netid__iexact=uname)


def oauth_handler(request):
    print(request.GET)
    return HttpResponse("Hi!")
