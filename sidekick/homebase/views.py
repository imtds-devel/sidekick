# -*- coding: utf-8 -*-
from sidekick import views
from django.http import HttpResponseRedirect
from django.shortcuts import render
from homebase.models import Announcements, Events, StaffStatus, Employees
from .forms import AnnouncmentForm, EventForm, StatusForm
from shifts.models import Shifts
import datetime
import pytz


def roster_test(request):
    locations = [
        {
            'name': 'Labs',
            'people': [
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='nchera13'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=22, minute=0),
                        'short_location':  'MAR',
                        'checkin': 'F',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='jwood14'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=18, minute=0),
                        'short_location':  'DAR',
                        'checkin': 'T',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='maytenfsu14'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'STA',
                        'checkin': 'T',
                    }
                },

            ]
        },
        {
            'name': 'Support Desk',
            'people': [
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='ewoods13'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=22, minute=0),
                        'short_location':  'REP',
                        'checkin': 'F',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='nfrasier12'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=18, minute=30),
                        'short_location':  'REP',
                        'checkin': 'T',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='dbartholomew13'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'REP',
                        'checkin': 'T',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='bduggan14'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'TEK',
                        'checkin': 'T',
                    }
                },

            ]
        },
        {
            'name': 'Repair Center',
            'people': [
                {
                    'type': 'mgr',
                    'employee': Employees.objects.get(netid='rsantoiemma'),
                    'shift': {
                        'short_location': 'MGR'
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='lkaakau14'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=18, minute=30),
                        'short_location':  'SST',
                        'checkin': 'T',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='asaguilar14'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'TEK',
                        'checkin': 'T',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='sbillideau15'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'TEK',
                        'checkin': 'F',
                    }
                },
                {
                    'type': 'stu',
                    'employee': Employees.objects.get(netid='ddubisz13'),
                    'shift': {
                        'isopen': False,
                        'start': datetime.datetime(year=2018, month=3, day=15, hour=16, minute=0),
                        'end': datetime.datetime(year=2018, month=3, day=15, hour=19, minute=0),
                        'short_location':  'TEK',
                        'checkin': 'T',
                    }
                },

            ]
        },
        {
            'name': 'East Campus',
            'people': [
                {
                    'type': 'stf',
                    'employee': Employees.objects.get(netid='aroberts'),
                    'shift': {
                        'short_location': 'STF'
                    }
                },
            ]
        },
        {
            'name': 'West Campus',
            'people': [
                {
                    'type': 'stf',
                    'employee': Employees.objects.get(netid='awood'),
                    'shift': {
                        'short_location': 'STF'
                    }
                },
            ]
        },
        {
            'name': 'Off Campus',
            'people': [
                {
                    'type': 'stf',
                    'employee': Employees.objects.get(netid='rtaylor'),
                    'shift': {
                        'short_location': 'STF'
                    }
                },
            ]
        },
        {
            'name': 'In Meeting',
            'people': [
                {
                    'type': 'mgr',
                    'employee': Employees.objects.get(netid='rdavis'),
                    'shift': {
                        'short_location': 'MGR'
                    }
                },
            ]
        },
        {
            'name': 'Out of Office',
            'people': [
                {
                    'type': 'stf',
                    'employee': Employees.objects.get(netid='bmonroe'),
                    'shift': {
                        'short_location': 'STF'
                    }
                },
                {
                    'type': 'stf',
                    'employee': Employees.objects.get(netid='rlucchesi'),
                    'shift': {
                        'short_location': 'STF'
                    }
                },
            ]
        },

    ]
    return views.load_page(request, "homebase/test.html", {'netid': 'nchera13', 'hb_loc_data': locations})


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
