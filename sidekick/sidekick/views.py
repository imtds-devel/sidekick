# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from roster.models import Trophies
from homebase.models import Employees


@login_required
def load_page(request, template, context):

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return "403 unauthorized user!"

    trophy_list = Trophies.objects.all()
    context['trophy_list'] = trophy_list

    return render(request, template, context)


def authorize(request):
    try:
        user = Employees.objects.get(netid=request.user.lower())
        return True
    except Exception:
        return False