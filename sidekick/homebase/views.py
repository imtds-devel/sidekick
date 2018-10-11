# -*- coding: utf-8 -*-
from sidekick import views
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from homebase.models import Employees, Announcements, Events, StaffStatus, NotifySources
from .forms import StatusForm
from shifts.models import Shifts
import datetime
import pytz
import json


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


def new_announcement(request):
    # Reject any non-POST request
    if request.method != "POST":
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    request = views.get_current_user(request)

    Announcements(
        announcer=Employees.objects.get(netid=str(request.user)),
        subject=request.POST.get('subject', None),
        body=request.POST.get('body', None)
    ).save()

    return JsonResponse({
        'result': 'success',
        'desc': 'Announcement was added successfully'
    })


def new_event(request):
    # Reject any non-POST request
    if request.method != "POST":
        return JsonResponse({
            'result': 'failure',
            'desc': 'Bad request method'
        }, status=500)

    request = views.get_current_user(request)

    Events(
        announcer=Employees.objects.get(netid=str(request.user)),
        title=request.POST.get('title', None),
        location=request.POST.get('location', None),
        event_date=request.POST.get('date', None),
        description=request.POST.get('description', None)
    ).save()

    return JsonResponse({
        'result': 'success',
        'desc': 'Event was added successfully'
    })


def prep_context():
    announcement_list = Announcements.objects.all().order_by('posted')
    event_list = Events.objects.all().order_by('event_date')

    tz = pytz.timezone("America/Los_Angeles")
    now = tz.localize(datetime.datetime.now())
    shifts = Shifts.objects.filter(shift_start__lte=now).filter(shift_end__gt=now).order_by('location')
    labs = []
    support = []
    rep = []
    to_check_in = []

    for shift in shifts:
        if shift.location == 'ma' or shift.location == 'da' or shift.location == 'st':
            labs.append(shift)
            to_check_in.append(shift)
        elif shift.location == 'sd' or shift.location == 'rc':
            support.append(shift)
            to_check_in.append(shift)
        elif shift.location == 'sr':
            rep.append(shift)

    staff_stats = StaffStatus.objects.all().order_by('netid')

    ordered_list = order(announcement_list, event_list)
    s_form = StatusForm()

    return {
        'shifts': shifts,
        'check_shifts': to_check_in,
        'lab_shifts': labs,
        'support_shifts': support,
        'rep_shifts': rep,
        'ordered_list': ordered_list,
        's_form': s_form,
        'staff_stats': staff_stats,
    }


def order(a_list, e_list):
    ordered = list(a_list) + list(e_list)
    # Combines the two lists, then sorts using lambda function with the announcement posted
    # attribute and event event_start attribute
    ordered_list = sorted(ordered, key=lambda x: x.posted.date() if hasattr(x, 'posted') else x.event_date, reverse=True)
    return ordered_list[:8]


def post_checkin(request):
    # Make sure it's a post request

    if not request.method == 'POST':
        return HttpResponse(
            json.dumps({"status": "Failed!"}),
            content_type="application/json"
        )

    request = views.get_current_user(request)
    shift_ids = request.POST.getlist('shift_ids[]')
    check_times = request.POST.getlist('check_times[]')

    # iterates through shift_ids and event_ids so they match up accordingly
    for count in range(0, len(shift_ids)):
        if shift_ids[count] is not None:
            shift = Shifts.objects.get(event_id=shift_ids[count])
        else:
            return HttpResponse(
                json.dumps({"status": "Failed! Shift id not found"}),
                content_type="application/json"
            )

        shift.checked_in = 'T'

        formattedTime = datetime.datetime.combine(shift.shift_date, datetime.datetime.strptime(check_times[count], '%H:%M').time())

        shift.checkin_time = formattedTime

        print(shift)
        shift.save()


    return HttpResponse(
        json.dumps({"status": "Check in successfully made!"}),
        content_type="application/json"
    )