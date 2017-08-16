# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from homebase.models import Employee

# Create your views here.
def index(request):
    #employee = get_object_or_404(models.Employee, pk='netid')
    employee_list = Employee.objects.all()
    context = {'employee_list':employee_list}
    return render(request, 'roster/index.html', context)