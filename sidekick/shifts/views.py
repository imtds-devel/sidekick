# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sidekick import views
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from shifts.functions.push_covers import push_cover
from .models import Shifts
from django.http import JsonResponse

user = 'jwood14' # This is hard coded, we don't want this hard coded TODO Make this not hardcoded

def index(request):
    # We import the current time
    now = timezone.now()
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

    #shifts_list = Shifts.objects.all().order_by('shift_start')

    #date = datetime.date.today()
    #current_week_day_iso = date.isocalendar()[2]
    #thisWeekIso = now.
    #context = {'shifts': shifts}
    context = {"date" : now}
    return views.load_page(request, 'shifts/index.html', context)

def filter_shifts(request):
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
