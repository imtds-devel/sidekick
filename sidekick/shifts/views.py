# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sidekick import views
from django.utils import timezone
from datetime import timedelta
from shifts.functions.push_covers import push_cover
from .models import Shifts

# Create your views here.
def index(request):
    # We import the current time
    # This is used to import
    now = timezone.now()
    current_week_day_iso = now.isocalendar()[2]
    sunday_start_date_current_week = now - timedelta(days=current_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    shifts_this_week = Shifts.objects.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)

    #date = datetime.date.today()
    #current_week_day_iso = date.isocalendar()[2]
    #thisWeekIso = now.
    #context = {'shifts': shifts}
    context = {"the_week" : shifts_this_week }
    return views.load_page(request, 'shifts/index.html', context)

