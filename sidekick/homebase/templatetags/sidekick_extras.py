from django import template
from django.template.defaultfilters import stringfilter

from sidekick.access import get_access

register = template.Library()

# NOTE: This is a universal template filter that's used in all our pages, but it has to be located in an app
#   so I'm putting it here

# HOW TO USE THIS FILTER
# It accepts a string with a netid and a string with the access area
# Format it like so:
# user|has_access:"access_area"
# This returns a bool val, so ideally you'd control access to a portion of the site by pairing this with an 'if' tag
@register.filter(name="has_access")
@stringfilter
def has_access(netid, area):
    return get_access(netid, area)
