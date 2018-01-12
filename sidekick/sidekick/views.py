# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from roster.models import Trophies

def load_page(request, template, context):
    trophy_list = Trophies.objects.all()
    context['trophy_list'] = trophy_list

    return render(request, template, context)