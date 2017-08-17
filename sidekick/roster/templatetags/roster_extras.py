from django import template
from sidekick.settings import STATIC_URL
import urllib


register = template.Library()

@register.filter(name='img_exists')
def img_exists(filepath):
    try:
        urllib.request.urlopen(STATIC_URL+filepath)
        return filepath
    except:
        index = filepath.rfind('/')
        new_filepath = filepath[:index] + '/default.jpg'
        return new_filepath
