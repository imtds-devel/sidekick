from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


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