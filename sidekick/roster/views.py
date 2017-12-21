# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from sidekick import views
from homebase.models import Employees
from .models import Proficiencies, Discipline
from .forms import EmployeeForm, StarForm, CommentForm
from sidekick.access import get_access
import json


# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":

        import copy
        data = copy.copy(request.POST)

        # In case we're not in production
        # Remove this line before production!
        request = views.get_current_user(request)

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


def post_comment(request):
    # Make sure it's a post request
    if not request.method == 'POST':
        return HttpResponse(
            json.dumps({"status": "Failed!"}),
            content_type="application/json"
        )

    # Make sure the user has proper access rights to do this
    request = views.get_current_user(request)
    poster = request.user
    about = request.POST.get('about', None)

    if about is not None:
        emp = Employees.objects.get(netid=about)
        if emp.position == 'lbt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access"}),
            content_type="application/json"
        )

    if not get_access(poster, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access"}),
            content_type="application/json"
        )

    # Finish getting variables
    subject = request.POST.get('subject', None)
    body = request.POST.get('body', None)

    # Construct discipline object
    comment = Discipline(
        subject=subject,
        poster=Employees.objects.get(netid=poster),
        about=Employees.objects.get(netid=about),
        description=body,
    )
    print(comment)
    comment.save()
    return HttpResponse(
        json.dumps({"status": "Comment successfully created!"}),
        content_type="application/json"
    )


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
