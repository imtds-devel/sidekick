# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from sidekick import views
from homebase.models import Employee
from .forms import EmployeeForm


# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'roster/index.html', prep_context())


# Helper Functions

def prep_context():
    employee_list = Employee.objects.all().order_by('lname')
    form = EmployeeForm()
    return {
        'employee_list': employee_list,
        'form': form
    }
