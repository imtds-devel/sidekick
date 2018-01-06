# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from roster.models import Trophies
from homebase.models import Employees

live = False  # Set to true for production!

# @login_required # UNCOMMENT THIS BEFORE GOING LIVE
def load_page(request, template, context):

    request = get_current_user(request)

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return HttpResponse("403 unauthorized user!")

    context['user_img'] = "employees/"+str(request.user)+".gif"
    context['user_netid'] = str(request.user)
    context['user_name'] = Employees.objects.get(netid__iexact=str(request.user)).full_name

    trophy_list = Trophies.objects.all()
    context['trophy_list'] = trophy_list

    return render(request, template, context)


def get_current_user(request):
    if not live:
        request.user = set_user_string(request.user)

    return request


def set_user_string(user):
    if not live:
        return "ddubisz13"
    else:
        return user


def authorize(request):
    uname = str(request.user)
    return Employees.objects.filter(netid__iexact=uname)
