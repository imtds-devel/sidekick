from django import template
<<<<<<< HEAD
from sidekick.settings import STATIC_URL
import urllib
=======
import os
# from sidekick.settings import STATIC_URL
# import urllib
>>>>>>> 310e1181dbcb27240a4c5b904e400afba41c0393


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
