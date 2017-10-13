# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from roster.models import Trophies
from homebase.models import Employees


# @login_required # UNCOMMENT THIS BEFORE GOING LIVE
def load_page(request, template, context):

    request = get_current_user(request) # COMMENT THIS BEFORE GOING LIVE

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return HttpResponse("403 unauthorized user!")


    context['user_img'] = "employees/"+str(request.user)+".gif"
    context['user_name'] = Employees.objects.get(netid__iexact=str(request.user)).full_name


    trophy_list = Trophies.objects.all()
    context['trophy_list'] = trophy_list

    return render(request, template, context)

def get_current_user(request):
    live = False
    if not live:
        request.user = 'bduggan14'

    return request

def authorize(request):
    uname = str(request.user)
    return Employees.objects.filter(netid__iexact=uname)

