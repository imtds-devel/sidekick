# -*- coding: utf-8 -*-
from sidekick import views
from django.http import HttpResponseRedirect, JsonResponse
from homebase.models import Employees, Announcements, Events, StaffStatus
from .forms import StatusForm
from shifts.models import Shifts
import datetime
import pytz


def index(request):
    # If this is a form submission
    if request.method == "POST":
        # Need to validate which form is being submitted (give the input a name attribute)
        import copy
        data = copy.copy(request.POST)

        form = None

        if 's-form' in request.POST:
            status = StaffStatus.objects.get(netid=request.POST['netid'])
            form = StatusForm(data, instance=status)
            print(form.fields)

        if form is not None and form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print("Bad form!")

    return views.load_page(request, 'homebase/index.html', prep_context())


def add_announcement(request):
    # Reject any non-POST request
    if request.method != "POST":
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    Announcements(
        announcer=Employees.objects.get(netid=str(request.user)),
        subject=request.POST.get('subject', None),
        body=request.POST.get('body', None)
    ).save()

    return JsonResponse({
        'result': 'success',
        'desc': 'Announcement was added successfully'
    })


def add_event(request):
    return True


def prep_context():
    announcement_list = Announcements.objects.all().order_by('posted')
    event_list = Events.objects.all().order_by('event_start')

    tz = pytz.timezone("America/Los_Angeles")
    now = tz.localize(datetime.datetime.now())
    shifts = Shifts.objects.filter(shift_start__lte=now).filter(shift_end__gt=now).order_by('location')
    labs = []
    support = []

    for shift in shifts:
        if shift.location == 'ma' or shift.location == 'da' or shift.location == 'st':
            labs.append(shift)
        elif shift.location == 'sd' or shift.location == 'rc':
            support.append(shift)

    staff_stats = StaffStatus.objects.all().order_by('netid')

    ordered_list = order(announcement_list, event_list)
    s_form = StatusForm()
    return {
        'lab_shifts': labs,
        'support_shifts': support,
        'ordered_list': ordered_list,
        's_form': s_form,
        'staff_stats': staff_stats,
    }


def order(a_list, e_list):
    ordered = list(a_list) + list(e_list)
    # Combines the two lists, then sorts using lambda function with the announcement posted
    # attribute and event event_start attribute
    ordered_list = sorted(ordered, key=lambda x: x.posted.date() if hasattr(x, 'posted') else x.event_start, reverse=True)
    return ordered_list[:8]
