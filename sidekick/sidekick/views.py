# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sidekick.settings import PRODUCTION
from django.http import HttpResponse, JsonResponse
from roster.models import Trophies
from homebase.models import Employees, ModTasks
from shifts.models import Shifts
import datetime
import pytz


# @login_required # UNCOMMENT THIS BEFORE GOING LIVE
def load_page(request, template: str, context: dict):

    request = get_current_user(request)

    # Check to make sure authenticated user is authorized to access the webpage
    if not authorize(request):
        return HttpResponse("403 unauthorized user!")

    tz = pytz.timezone("America/Los_Angeles")
    now = tz.localize(datetime.datetime.now())

    curr_user = Employees.objects.get(netid__iexact=str(request.user))
    context['user'] = curr_user
    context['user_name'] = curr_user.full_name
    context['user_img'] = "employees/"+str(curr_user.netid)+".gif"
    context['user_netid'] = str(curr_user.netid)
    context['curr_mod'] = Shifts.objects.filter(
        location='md',
        shift_start__lte=now,
        shift_end__gt=now,
        is_open=False,
        owner__isnull=False,
    ).first()
    context['next_mod'] = Shifts.objects.filter(
        location='md',
        shift_start__gt=now,
        is_open=False,
        owner__isnull=False,
    ).order_by('shift_start').first()
    context['my_shift'] = Shifts.objects.filter(
        owner=curr_user,
        shift_end__gte=now,
        is_open=False
    ).order_by('shift_start').first()
    if context['my_shift']:
        # If someone is graduating, there will come a point when they don't have any upcoming shifts
        # We don't want the site to crash for them if/when this happens!
        context['my_shift_happening'] = tz.localize(context['my_shift'].shift_start) < now

    context['trophy_list'] = Trophies.objects.filter(recipient=curr_user)
    context['curr_page'] = template.split("/")[0]
    context['tasks'] = ModTasks.objects.filter(completed=False).order_by('created_date')
    context['completed_tasks'] = ModTasks.objects.filter(completed=True).order_by('-completed_date')
    context['modnote'] = ModNote.objects
    return render(request, template, context)


def get_current_user(request):
    if not PRODUCTION:
        request.user = set_user_string(request.user)

    return request


def set_user_string(user):
    if not PRODUCTION:
        return "cditter14"
    else:
        return user


def authorize(request):
    uname = str(request.user)
    return Employees.objects.filter(netid__iexact=uname, delete=False)


def oauth_handler(request):
    print(request.GET)
    return HttpResponse("Hi!")

def new_task(request):
    # Reject any non-POST request
    if request.method != 'POST':
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    request = views.get_current_user(request)

    ModTasks(
        poster=Employees.objects.get(netid=str(request.user)),
        task=request.POST.get('task', None),
    ).save()

    return JsonResponse({
        'result': 'success',
        'desc': 'Task was added successfully'
    })

def complete_task(request):
    # Reject any non-POST request
    if request.method != 'POST':
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    request = views.get_current_user(request)
    tasktext = request.POST.get('task', None)
    if tasktext is not None:
        task = ModTasks.objects.get(task=tasktext)
        task.completer = Employees.objects.get(netid=str(request.user))
        task.completed_date = datetime.datetime.now()
        task.completed = True
        print(task)
        task.save()
        return JsonResponse({
            'result': 'success',
            'desc': 'Task was completed successfully'
        })
    else:
        return JsonResponse({
            'result': 'Failed',
            'desc': 'No task was selected'
        })

def update_note(request):
    # Reject any non-POST request
    if request.method != 'POST':
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    request = views.get_current_user(request)
    notetext = request.POST.get('note', None)
    if notetext is not None:
        note = ModTasks.objects.get(id='1')
        note.note = notetext
        note.poster = Employees.objects.get(netid=str(request.user))
        note.created_date = datetime.datetime.now
        print(note)
        note.save()
        return JsonResponse({
            'result': 'success',
            'desc': 'Note was updated successfully'
        })
    else:
        return JsonResponse({
            'result': 'Failed',
            'desc': 'No note was selected'
        })