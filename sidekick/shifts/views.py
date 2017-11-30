# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz
from sidekick import views
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from shifts.functions.push_covers import push_cover
from .models import Shifts
from .models import ShiftCovers
from homebase.models import Employees
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import TimeField
from django.utils.timezone import make_aware, make_naive

user = 'jwood14' # This is hard coded, we don't want this hard coded TODO Make this not hardcoded
user_position = Employees.objects.get(netid=user).position

def index(request):
    # The possible locations for a shift in the database 
    shift_classifer = {
        'lbt': "Lab Tech",
        'llt': "Lead Lab Tech",
        'spt': "Support Tech",
        'sst': "Senior Support Tech",
        'sdr': "Support Desk Rep",
        'mgr': "Manager",
        'ma': "Marshburn",
        'da': "Darling",
        'st': "Stamps",
        'rc': "Repair Center",
        'sd': "Support Desk",
    }

    # We import the current time
    now = timezone.now()
    '''
    given_week_day_iso = now.isocalendar()[2]
    # if currently is sunday
    if given_week_day_iso == 7:
        sunday_start_date_current_week = now
    else:
        sunday_start_date_current_week = now - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    week = [] # start empty
    for day in range(0, 7):
        week.append(sunday_start_date_current_week + timedelta(days=day))
    '''
    #shifts_list = Shifts.objects.all().order_by('shift_start')

    #date = datetime.date.today()
    #current_week_day_iso = date.isocalendar()[2]
    #thisWeekIso = now.
    #context = {'shifts': shifts}
    context =   {"date" : now,
                "locations" : shift_classifer,
                "user_position" : user_position}
    return views.load_page(request, 'shifts/index.html', context)

def filter_user_shifts(request):
    option = request.GET.get('option', None) # Retreive the option
    date_string = request.GET.get('date', None) # Retreive the date entered
    date = datetime.strptime(date_string, '%Y-%m-%d') # Make that string into a datetime object
    queryset = Shifts.objects.filter(owner = user).order_by('shift_start') # We filter the query set down to the shifts owned by user logged in

    if option == 'next':
        date = date + timedelta(days=7)
    elif option == 'prev':
        date = date - timedelta(days=7)

    given_week_day_iso = date.isocalendar()[2]
    # if currently is sunday
    if given_week_day_iso == 7:
        sunday_start_date_current_week = date
    else:
        sunday_start_date_current_week = date - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    filtered_shifts = queryset.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)
    translated_shifts = filtered_shifts.values('id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open','checked_in', 'google_id', 'permanent')
    week = [] # start empty
    for day in range(0, 7):
        week.append(sunday_start_date_current_week + timedelta(days=day))
    data = {
        'date' : str(date),
        'shifts' : list(translated_shifts),
        'week' : week
    }
    return JsonResponse(data)

def filter_open_shifts(request):
    option = request.GET.get('option', None) # Retreive the option
    date_string = request.GET.get('date', None) # Retreive the date entered
    location = request.GET.get('location', None) # Retreive the desired location of open shifts
    date = datetime.strptime(date_string, '%Y-%m-%d') # Parse that string into a datetime object
    queryset = Shifts.objects.filter(is_open = True)

    # If the location is a simple location
    if location in ['ma', 'da', 'st', 'rc', 'sd', 'sst']:
        queryset = queryset.filter(location = location).order_by('shift_start') # We filter the query set down to the shifts in that location
    # Otherwise, we need to determine by position, and filter with the corresponding locations
    else:
        if location in ['lbt', 'llt']: # If they are a labtech we need to show all shifts in the libraries
            queryset = queryset.filter(Q(location='ma') | Q(location='da') | Q(location='st')).order_by('shift_start')
        elif location == 'spt': # If support tech
            queryset = queryset.filter(Q(location='rc') | Q(location='sd')).order_by('shift_start')
        elif location == 'sdr': # If support desk rep
            queryset = queryset.filter(location='sr').order_by('shift_start')
        elif location == 'mgr': # If manager
            queryset = queryset.filter(location='md').order_by('shift_start')
        else: # This shouldn't be possible, but in this case I am not filtering by location
            queryset = queryset.order_by('shift_start')
            
    if option == 'next':
        date = date + timedelta(days=7)
    elif option == 'prev':
        date = date - timedelta(days=7)

    given_week_day_iso = date.isocalendar()[2]
    # if currently is sunday
    if given_week_day_iso == 7:
        sunday_start_date_current_week = date
    else:
        sunday_start_date_current_week = date - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    filtered_shifts = queryset.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)
    open_query_set = ShiftCovers.objects.all().select_related('shift')
    print (open_query_set)
    translated_shifts = filtered_shifts.values('id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open','checked_in', 'google_id', 'permanent')
    week = [] # start empty
    for day in range(0, 7):
        week.append(sunday_start_date_current_week + timedelta(days=day))
    data = {
        'date' : str(date),
        'shifts' : list(translated_shifts),
        'week' : week
    }
    return JsonResponse(data)

def filter_near_shifts(request):
    # Get the shift of the given id
    shift_id = request.GET.get('shiftID', None)
    this_shift = Shifts.objects.get(id=shift_id)
    # First we filter all shifts of the same location
    filtered_shifts = Shifts.objects.filter(location=this_shift.location)
    # Then we filter based on shifts that are occuring directly before or after the given shift
    filtered_shifts = filtered_shifts.filter(Q(shift_end=this_shift.shift_start) | Q(shift_start=this_shift.shift_end)).order_by('shift_start')

    # If the count is 2 then we should have exactly 2 shifts (one before and one after)
    # This allows us to create a range from the shift before to the shift after
    if filtered_shifts.count() == 2:
        start = filtered_shifts.first().shift_start
        end = filtered_shifts.last().shift_end
        print (start)
        print (end)
    elif filtered_shifts.count() == 1:
        start = filtered_shifts.first().shift_start
        end = this_shift.shift_end
        print (start)
        print (end)
    else:
        start = this_shift.shift_start
        end = this_shift.shift_end
        print (start)
        print (end)

    naive_start = make_naive(start)
    naive_end = make_naive(end)
    print (naive_start)
    print (naive_end)
    translated_shifts = filtered_shifts.values('id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open','checked_in', 'google_id', 'permanent')
    data = {
        'shifts' : list(translated_shifts)
    }
    return JsonResponse(data)