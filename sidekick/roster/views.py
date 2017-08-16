# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views


# Create your views here.
def index(request):
    employee_list = Employee.objects.all()
    context = {'employee_list':employee_list}
    return views.load_page(request, 'roster/index.html', context)
