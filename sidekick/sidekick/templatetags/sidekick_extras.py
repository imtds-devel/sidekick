from django import template
from django.template.defaultfilters import stringfilter

from sidekick.access import get_access

register = template.Library()

# HOW TO USE THIS FILTER
# It accepts a string with a netid and a string with the access area
# Format it like so:
# user|has_access:"access_area"
# This returns a bool val, so ideally you'd control access to a portion of the site by pairing this with an 'if' tag
@register.filter
@stringfilter
def has_access(netid, area):
    return get_access(netid, area)
