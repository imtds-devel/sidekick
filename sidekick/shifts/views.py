# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sidekick import views
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from shifts.functions.push_covers import push_cover
from .models import Shifts
from django.http import JsonResponse

# Create your views here.
shifts_list = Shifts.objects.all().order_by('shift_start')

def index(request):
    # We import the current time
    now = timezone.now()

    #shifts_list = Shifts.objects.all().order_by('shift_start')

    #date = datetime.date.today()
    #current_week_day_iso = date.isocalendar()[2]
    #thisWeekIso = now.
    #context = {'shifts': shifts}
    context = { "shifts" : shifts_list,
                "date" : now}
    return views.load_page(request, 'shifts/index.html', context)

def filter_shifts(request):
    dateString = request.GET.get('date', None)
    date = datetime.strptime(dateString, '%Y-%m-%d')
    queryset = Shifts.objects.all().order_by('shift_start')
    given_week_day_iso = date.isocalendar()[2]
    # if currently is sunday
    if given_week_day_iso == 7:
        sunday_start_date_current_week = date
    else:
        sunday_start_date_current_week = date - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    filteredShifts = queryset.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)
    translatedShifts = filteredShifts.values('id', 'title', 'owner', 'shift_date', 'shift_start', 'shift_end', 'location', 'is_open','checked_in', 'google_id', 'permanent')
    week = [] # start empty
    for day in range(0, 7):
        week.append(sunday_start_date_current_week + timedelta(days=day))
    data = {
        'shifts' : list(translatedShifts),
        'week' : week
    }
    return JsonResponse(data)
