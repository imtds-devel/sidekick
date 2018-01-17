# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from sidekick import views
from homebase.models import Employees
from .models import Proficiencies, Discipline, Trophies
from .forms import EmployeeForm, StarForm, CommentForm, DisciplineForm
from sidekick.access import get_access
import json
from django.http import JsonResponse


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


def update_bio(request):
    # Make sure it's a post request
    if not request.method == 'POST':
        return HttpResponse(
            json.dumps({"status": "Failed!"}),
            content_type="application/json"
        )

    # Make sure the user has proper access rights to do this
    request = views.get_current_user(request)
    updater = request.user
    about = request.POST.get('about', None)

    print(request.user)

    if about is not None:
        emp = Employees.objects.get(netid=updater)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(1)"}),
            content_type="application/json"
        )

    if not get_access(updater, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(2)"}),
            content_type="application/json"
        )

    # Finish getting variables
    fname = request.POST.get('fname', None)
    lname = request.POST.get('lname', None)
    apuid = request.POST.get('apuid', None)
    phone = request.POST.get('phone', None)
    code = request.POST.get('code', None)
    bday = request.POST.get('bday', None)
    position = request.POST.get('position', None)
    pos_desc = request.POST.get('pos_desc', None)
    standing = request.POST.get('standing', None)
    developer = request.POST.get('developer', None)

    # Construct discipline object
    employee = Employees.objects.get(netid=about)

    employee.fname = fname
    employee.lname = lname
    employee.phone = phone
    employee.apuid = apuid
    employee.codename = code
    employee.position = position
    employee.position_desc = pos_desc
    employee.standing = standing
    employee.birthday = bday
    employee.developer = developer

    print(employee)
    employee.save()
    return HttpResponse(
        json.dumps({"status": "Bio successfully updated!"}),
        content_type="application/json"
    )


def update_prof(request):
    # Make sure it's a post request
    if not request.method == 'POST':
        return HttpResponse(
            json.dumps({"status": "Failed!"}),
            content_type="application/json"
        )

    # Make sure the user has proper access rights to do this
    request = views.get_current_user(request)
    updater = request.user
    about = request.POST.get('about', None)

    print(request.user)

    if about is not None:
        emp = Employees.objects.get(netid=updater)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(1)"}),
            content_type="application/json"
        )

    if not get_access(updater, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(2)"}),
            content_type="application/json"
        )

    # Finish getting variables
    basic = request.POST.get('basic', None)
    adv = request.POST.get('adv', None)
    field = request.POST.get('field', None)
    printer = request.POST.get('print', None)
    net = request.POST.get('net', None)
    mobile = request.POST.get('mobile', None)
    ref = request.POST.get('ref', None)
    soft = request.POST.get('soft', None)

    # Construct discipline object
    profic = Proficiencies.objects.get(netid=about)
    profic.basic = basic
    profic.advanced = adv
    profic.field = field
    profic.printer = printer
    profic.network = net
    profic.mobile = mobile
    profic.refresh = ref
    profic.software = soft

    print(profic)
    str(profic).save()
    return HttpResponse(
        json.dumps({"status": "Proficiencies successfully updated!"}),
        content_type="application/json"
    )


def post_award(request):
    # Make sure it's a post request
    if not request.method == 'POST':
        return HttpResponse(
            json.dumps({"status": "Failed!"}),
            content_type="application/json"
        )

    # Make sure the user has proper access rights to do this
    request = views.get_current_user(request)
    giver = request.user
    recipient = request.POST.get('recipient', None)

    print(request.user)

    if recipient is not None:
        emp = Employees.objects.get(netid=giver)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(1)"}),
            content_type="application/json"
        )

    if not get_access(giver, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(2)"}),
            content_type="application/json"
        )

    # Finish getting variables
    name = request.POST.get('name', None)
    reason = request.POST.get('reason', None)
    award = request.POST.get('type', None)

    # Construct discipline object
    award = Trophies(
        name=name,
        trophy_type=award,
        giver=Employees.objects.get(netid=giver),
        recipient=Employees.objects.get(netid=recipient),
        reason=reason,
    )
    print(award)
    award.save()
    return HttpResponse(
        json.dumps({"status": "Award successfully created!"}),
        content_type="application/json"
    )


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
        emp = Employees.objects.get(netid=poster)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(1)"}),
            content_type="application/json"
        )

    if not get_access(poster, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access(2)"}),
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


def post_discipline(request):
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
        emp = Employees.objects.get(netid=poster)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
        print(access_area)
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! About netid not found"}),
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
    extent = request.POST.get('extent', None)

    # Construct discipline object
    comment = Discipline(
        subject=subject,
        poster=Employees.objects.get(netid=poster),
        about=Employees.objects.get(netid=about),
        val=extent,
        description=body,
    )
    print(comment)
    comment.save()
    return HttpResponse(
        json.dumps({"status": "Comment successfully created!"}),
        content_type="application/json"
    )


def get_comments(request):
    netid = request.GET.get('netid', None)

    comments = Discipline.objects.filter(about_id=netid)

    translated_comments = comments.values('about_id', 'subject', 'val', 'time', 'description')

    translated_comments = [{
        'about_id': comment.about_id,
        'subject': comment.subject,
        'val': comment.val,
        'time': comment.time.strftime("%m/%d/%y"),
        'description': comment.description
    } for comment in comments]

    data = {
        'comlist': list(translated_comments)
    }

    return JsonResponse(data)


def get_trophies(request):
    netid = request.GET.get('netid', None)

    trophies = Trophies.objects.filter(recipient=netid)

    translated_trophies = [{
        'giver': str(trophy.giver),
        'reason': str(trophy.reason),
        'name': trophy.name,
        'trophy_type': trophy.trophy_type,
        'url': trophy.url
    } for trophy in trophies]

    data = {
        'trophlist': list(translated_trophies)
    }

    return JsonResponse(data)


def delete_employee(request):
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
        emp = Employees.objects.get(netid=poster)
        if emp.position == 'llt':
            access_area = 'roster_modfb_lab'
        else:
            access_area = 'roster_modfb_all'
        print(access_area)
    else:
        return HttpResponse(
            json.dumps({"status": "Failed! About netid not found"}),
            content_type="application/json"
        )

    if not get_access(poster, access_area):
        return HttpResponse(
            json.dumps({"status": "Failed! User does not have access"}),
            content_type="application/json"
        )

    # Construct discipline object
    employee = Employees.objects.get(netid=about)
    employee.delete = True
    print(employee)
    employee.save()
    return HttpResponse(
        json.dumps({"status": "Employee successfully deleted!"}),
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
