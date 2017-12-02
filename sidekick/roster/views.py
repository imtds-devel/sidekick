# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from sidekick import views
from homebase.models import Employees
from .models import Proficiencies
from .forms import EmployeeForm
from .forms import CommentForm
from .forms import StarForm


# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":

        import copy
        data = copy.copy(request.POST)

        # In case we're not in production
        # Remove this line before production!
        #request = views.get_current_user(request)

        data['poster'] = request.user
        form = CommentForm(data)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        data['giver'] = request.user
        form = StarForm(data)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'roster/index.html', prep_context())


# Helper Functions

def prep_context():
    employee_list = Employees.objects.all().order_by('lname')
    empform = EmployeeForm()
    comform = CommentForm()
    starform = StarForm()


    emp_tuple = []
    for emp in employee_list:
        prof = Proficiencies.objects.filter(netid=emp.netid)
        emp_tuple.append((emp, prof))

    return {
        'employee_list': emp_tuple,
        'empform': empform,
        'comform': comform,
        'starform': starform
    }
