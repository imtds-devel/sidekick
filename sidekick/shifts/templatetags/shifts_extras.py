''' shifts_extras offers filters for the shifts on the shift page, each has a description to describe 
it's individual function and use case.'''
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def week_of(value, arg):
    '''Filters shifts that occur during the week containing the given date, note that we prefer 
    weeks to start with Sundayso we have to adjust ISO accordingly. Returns a subset of shifts.
    Usage: {{shifts|week_of:"ISO DATE"}} '''
    #TODO ENSURE ARG IS A DATETIME INSTANCE 
    given_week_day_iso = arg.isocalendar()[2]
    sunday_start_date_current_week = arg - timedelta(days=given_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    return value.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)

@register.filter
def this_week(value):
    '''Filters this week's shifts. Note that we make weeks start with Sunday so we adjust ISO accordingly.
    Returns a subset of shifts that occur during the current week.
    Usage: {{shifts|this_week}}'''
    now = timezone.now()
    current_week_day_iso = now.isocalendar()[2]
    sunday_start_date_current_week = now - timedelta(days=current_week_day_iso)
    end_of_week = sunday_start_date_current_week + timedelta(days=6)
    return value.filter(shift_date__gte=sunday_start_date_current_week, shift_date__lte=end_of_week)