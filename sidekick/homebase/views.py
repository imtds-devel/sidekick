# -*- coding: utf-8 -*-
from sidekick import views
from django.http import HttpResponseRedirect, HttpResponse
from homebase.models import Announcements, Events, StaffStatus
from .forms import AnnouncmentForm, EventForm, StatusForm
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
        if 'e-form' in request.POST:
            # In case we're not in production
            # Remove this line before production!
            request = views.get_current_user(request)
            data['announcer'] = str(request.user)
            form = EventForm(data)
            print(form.fields)

        if 'a-form' in request.POST:
            # In case we're not in production
            # Remove this line before production!
            request = views.get_current_user(request)
            data['announcer'] = str(request.user)
            form = AnnouncmentForm(data)
            print(form)

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
    a_form = AnnouncmentForm()
    e_form = EventForm()
    s_form = StatusForm()
    return {
        'shifts': shifts,
        'lab_shifts': labs,
        'support_shifts': support,
        'ordered_list': ordered_list,
        'a_form': a_form,
        'e_form': e_form,
        's_form': s_form,
        'staff_stats': staff_stats,
    }


def order(a_list, e_list):
    ordered = list(a_list) + list(e_list)
    # Combines the two lists, then sorts using lambda function with the announcement posted
    # attribute and event event_start attribute
    ordered_list = sorted(ordered, key=lambda x: x.posted.date() if hasattr(x, 'posted') else x.event_start, reverse=True)
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

    print(shift_ids)
    print(check_times)

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

        formattedTime = str(shift.shift_date) + " " + check_times[count]
        print("formatted time " + formattedTime)

        shift.checkin_time = formattedTime

        print(shift)
        shift.save()


    return HttpResponse(
        json.dumps({"status": "Check in successfully made!"}),
        content_type="application/json"
    )