''' shifts_extras offers filters for the shifts on the shift page, each has a description to describe 
it's individual function and use case.'''
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def datetime_to_date(value):
    '''Filters the now to a date that can be the default for the selector
    Usage: {{date|datetime_to_date}} '''
    day = value.strftime('%Y-%m-%d')
    return day