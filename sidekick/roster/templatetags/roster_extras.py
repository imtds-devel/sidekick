from django import template
from sidekick.settings import STATIC_URL
import urllib
import os
# from sidekick.settings import STATIC_URL
# import urllib


register = template.Library()


@register.filter(name='img_exists')
def img_exists(filepath):
    """ # For use if hosting static content in a remote location

    try:
        urllib.request.urlopen(STATIC_URL+filepath)
        return filepath
    except:
        index = filepath.rfind('/')
        new_filepath = filepath[:index] + '/default.jpg'
        return new_filepath

    """
    # For use if hosting static content locally
    if os.path.isfile(os.getcwd()+"/static/"+filepath):
        return filepath
    else:
        index = filepath.rfind('/')
        new_filepath = filepath[:index] + '/default.jpg'
        return new_filepath



# this filter is the same as above but is only used on the homing beacon
# when shift data is pulled from Sling rather than the database
@register.filter(name='emp_img_exists')
def emp_img_exists(filepath):
    """ # For use if hosting static content in a remote location

    try:
        urllib.request.urlopen(STATIC_URL+filepath)
        return filepath
    except:
        index = filepath.rfind('/')
        new_filepath = filepath[:index] + '/default.jpg'
        return new_filepath

    """
    # For use if hosting static content locally
    if os.path.isfile(os.getcwd()+"/static/employees/"+filepath+".gif"):
        return "employees/"+filepath+".gif"
    else:
        index = filepath.rfind('/')
        new_filepath = '/default.jpg'
        return new_filepath
