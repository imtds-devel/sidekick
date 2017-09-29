# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from roster.models import Trophies
from homebase.models import Employees


@login_required
def load_page(request, template, context):

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return HttpResponse("403 unauthorized user!")


    context['user_netid'] = request.user
    context['user_name'] = Employees.objects.get(netid__iexact=str(request.user)).full_name


    trophy_list = Trophies.objects.all()
    context['trophy_list'] = trophy_list

    return render(request, template, context)


def authorize(request):
    uname = str(request.user)
    return Employees.objects.filter(netid__iexact=uname)
