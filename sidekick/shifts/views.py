# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from .functions.google_api import synchronize
from .functions.cover import push_cover, CoverInstructions
from .models import Shifts
from .models import ShiftCovers
from sidekick import views
from datetime import timedelta
from datetime import datetime
from homebase.models import Employees
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import TimeField
from django.http import HttpResponse
from django.utils.timezone import make_aware, make_naive
from sidekick.views import get_current_user
import pytz


def post_cover(request):
    """
    request.user = get_current_user(request)

    permanent = bool(request.POST.get('permanent', None))
    partial = bool(request.POST.get('partial', None))
    actor = Employees.objects.get(str(request.POST.get('owner', None)))  # This way, managers can post on others' behalf
    sob_story = str(request.POST.get('sob_story', None))
    if permanent:
        s_id = str(request.POST.get('permanent_id', None))
    else:
        s_id = str(request.POST.get('event_id', None))
    if partial:
        part_start = request.POST.get('part_start', None)
        part_end = request.POST.get('part_end', None)
    else:
        part_start = None
        part_end = None
    """
    permanent = True
    partial = False
    actor = Employees.objects.get(netid='nchera13')
    sob_story = "tst"
    s_id = "2um9rcro6hhk7bb0ttee4debb1"
    part_start = None
    part_end = None

    data = CoverInstructions(
        post=True,
        permanent=permanent,
        partial=partial,
        shift_id=s_id,
        actor=actor,
        start_time=part_start,
        end_time=part_end,
        sob_story=sob_story,
    )
    push_cover(data)
    return HttpResponse("Done!")


def take_cover(request):
    request.user = get_current_user(request)
    permanent = False
    partial = False
    actor = Employees.objects.get(netid='nchera13')
    sob_story = None
    s_id = "6ekqvdbqp5c8er4t1tdugk0k1s"
    part_start = None
    part_end = None

    data = CoverInstructions(
        post=False,
        permanent=permanent,
        partial=partial,
        shift_id=s_id,
        actor=actor,
        start_time=part_start,
        end_time=part_end,
        sob_story=sob_story,
    )
    push_cover(data)
    return HttpResponse("Done!")


def index(request):
    request_user = get_current_user(request)
    user = Employees.objects.get(netid=request_user.user)
    user_position = user.position

    # The possible positions for an employee in the database 
    positions = {
        'lbt': "Lab Tech",
        'llt': "Lead Lab Tech",
        'spt': "Support Tech",
        'sst': "Senior Support Tech",
        'sdr': "Support Desk Rep",
        'mgr': "Manager"
    }
    # The possible locations for a location in the database
    locations = {
        'ma': "Marshburn",
        'da': "Darling",
        'st': "Stamps",
        'rc': "Repair Center",
        'sd': "Support Desk",
        'md': "MoD Desk"
    }

    # We import the current time
    now = timezone.now()

    # Synchronize our db with the Google Cal
    synchronize(flush=False)

    # We build our context for the page
    context = {
        "date": now,
        "positions": positions,
        "locations": locations,
        "user_position": user_position
    }
    return views.load_page(request, 'shifts/index.html', context)


# This function responds to the AJAX request for user shifts
def filter_user_shifts(request):
    request_user = get_current_user(request)
    user = Employees.objects.get(netid=request_user.user)
    option = request.GET.get('option', None)  # Retrieve the option
    date_string = request.GET.get('date', None)  # Retrieve the date entered
    date = datetime.strptime(date_string, '%Y-%m-%d')  # Make that string into a datetime object
    # We filter the query set down to the shifts owned by user logged in
    queryset = Shifts.objects.filter(owner=user).order_by('shift_start')
    
    print (timezone.now())
    print (timezone.get_current_timezone())

    # The request can be contextual to the previous or next week, this is triggered when the user presses those buttons
    if option == 'next':
        date = date + timedelta(days=7)  # We add 7 days to the current date
    elif option == 'prev':
        date = date - timedelta(days=7)  # We remove 7 days from the current date

    # We get the iso date number, unfortunately, ISO believes that the week starts on Monday, so we have to work around
    given_week_day_iso = date.isocalendar()[2]
    # if currently is Sunday, remember ISO thinks Sunday is the last day of the week
    if given_week_day_iso == 7:
        sunday_start_date_current_week = date
    else:
        sunday_start_date_current_week = date - timedelta(days=given_week_day_iso)  # To find our Sunday start we subtract the current day of the week via timedelta
    end_of_week = sunday_start_date_current_week + timedelta(days=6)  # Then we add 6 to find end of this week, which is clearly a Saturday

    # next we will generate a "week" which will be a list of dates
    week = []  # start empty, we will build up the dates of each day
    for day in range(0, 7):  # day 1-7
        week.append(sunday_start_date_current_week + timedelta(days=day))  # Add each week date, Sunday to Saturday

    filtered_shifts = queryset.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)  # Now we filter the shifts to be the ones in the date range
    print (filtered_shifts)
    # We have to translate these shifts into these values so they can be JSON
    translated_shifts = filtered_shifts.values('event_id', 'title', 'owner','shift_date', 'shift_start','shift_end', 'location', 'is_open', 'checked_in', 'permanent_id')
    # This is the formatted data that we will be returning via AJAX
    print (translated_shifts)
    data = {
        'date': str(date),
        'shifts': list(translated_shifts),
        'week': week
    }
    # We return the data as JSON
    return JsonResponse(data)


# Similar to the filter user shifts, these filter the shifts that are open not the user's
def filter_open_shifts(request):
    request_user = get_current_user(request)
    user = Employees.objects.get(netid=request_user.user)
    option = request.GET.get('option', None)  # Retreive the option
    date_string = request.GET.get('date', None)  # Retreive the date entered
    location = request.GET.get('location', None)  # Retreive the desired location of open shifts
    date = datetime.strptime(date_string, '%Y-%m-%d')  # Parse that string into a datetime object
    queryset = Shifts.objects.filter(is_open = True)  # Retrieve the shifts that are open

    # If the location is a simple location
    if location in ['ma', 'da', 'st', 'rc', 'sd', 'ss']:
        queryset = queryset.filter(location = location).order_by('shift_start')  # We filter the query set down to the shifts in that location
    # Otherwise, we need to determine by position, and filter with the corresponding locations
    else:
        if location in ['lbt', 'llt']:  # If they are a labtech or lead labtech we need to show all library shifts
            queryset = queryset.filter(Q(location='ma') | Q(location='da') | Q(location='st')).order_by('shift_start')
        elif location == 'spt':  # If support tech
            queryset = queryset.filter(Q(location='rc') | Q(location='sd')).order_by('shift_start')
        elif location == 'sst':  # If senior support tech
            queryset = queryset.filter(location='ss')
        elif location == 'sdr':  # If support desk rep
            queryset = queryset.filter(location='sr').order_by('shift_start')
        elif location == 'mgr':  # If manager
            queryset = queryset.filter(location='md').order_by('shift_start')
        else:  # This shouldn't be possible, but in this case I am showing all shifts
            queryset = queryset.order_by('shift_start')

    # Contextual options
    if option == 'next':
        date = date + timedelta(days=7)
    elif option == 'prev':
        date = date - timedelta(days=7)

    # User shifts explains what is happening here pretty well
    given_week_day_iso = date.isocalendar()[2]
    # if currently is sunday
    if given_week_day_iso == 7:
        sunday_start_date_current_week = date
    else:
        sunday_start_date_current_week = date - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    filtered_shifts = queryset.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)
    translated_shifts = filtered_shifts.values('event_id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open', 'checked_in', 'permanent_id')
    week = []  # start empty
    for day in range(0, 7):
        week.append(sunday_start_date_current_week + timedelta(days=day))
    data = {
        'date': str(date),
        'shifts': list(translated_shifts),
        'week': week
    }
    return JsonResponse(data)


# This method responds to the AJAX request that is triggered by clicking an individual shift
def filter_near_shifts(request):
    request_user = get_current_user(request)
    user = Employees.objects.get(netid=request_user.user)
    # Get the shift of the given id
    shift_id = request.GET.get('shiftID', None)
    print(request.GET)
    print(shift_id)
    this_shift = Shifts.objects.get(event_id=shift_id)
    # First we filter all shifts of the same location
    filtered_shifts = Shifts.objects.filter(location=this_shift.location)
    # Then we filter based on shifts that are occuring directly before or after the given shift
    filtered_shifts = filtered_shifts.filter(Q(shift_end=this_shift.shift_start) | Q(shift_start=this_shift.shift_end)).order_by('shift_start')

    # If the count is 2 then we should have exactly 2 shifts (one before and one after)
    # This allows us to create a range from the shift before to the shift after
    if filtered_shifts.count() == 2:
        start = filtered_shifts.first().shift_start
        end = filtered_shifts.last().shift_end
        print(start)
        print(end)
    elif filtered_shifts.count() == 1:
        start = filtered_shifts.first().shift_start
        end = this_shift.shift_end
        print(start)
        print(end)
    else:
        start = this_shift.shift_start
        end = this_shift.shift_end
        print(start)
        print(end)

    naive_start = make_naive(start)
    naive_end = make_naive(end)
    print(naive_start)
    print(naive_end)
    # If this is an open shift, we also need the information from the corresponding shift_cover entry
    if this_shift.is_open:
        shift_cover = ShiftCovers.objects.get(shift=this_shift.event_id)
        translated_shift_cover = {
            'id': shift_cover.event_id,
            'poster': str(shift_cover.poster),
            'taker': str(shift_cover.taker),
            'type': shift_cover.type,
            'sobstory': shift_cover.sobstory,
            'post_date': shift_cover.post_date
        }
    else:
        translated_shift_cover = ['Not an Open Shift']
    # We construct a dictonary of the values contained in this shift
    translated_this_shift = {
        'event_id': this_shift.event_id,
        'title': this_shift.title,
        'owner': str(this_shift.owner),
        'shift_date': this_shift.shift_date,
        'shift_start': this_shift.shift_start,
        'shift_end': this_shift.shift_end,
        'location': this_shift.location,
        'is_open': this_shift.is_open,
        'checked_in': this_shift.checked_in,
        'permanent_id': this_shift.permanent_id
    }
    translated_shifts = filtered_shifts.values('event_id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open','checked_in', 'permanent_id')
    data = {
        'shiftCover': translated_shift_cover,
        'thisShift': translated_this_shift,
        'shifts': list(translated_shifts)
    }
    return JsonResponse(data)

# Create your views here.
def index(request):
    context = {}
    return views.load_page(request, 'shifts/index.html', context)
