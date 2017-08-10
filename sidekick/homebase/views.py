# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from .models import Employee

def index(request):
    employee_list = Employee.objects.all()
    context = {'employee_list':employee_list}
    return render(request, 'homebase/index.html', context)
