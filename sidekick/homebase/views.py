# -*- coding: utf-8 -*-
from sidekick import views
from homebase.models import Announcements

def index(request):
    return views.load_page(request, 'homebase/index.html', prep_context())

def prep_context():
    context = {}
    return views.load_page(request, 'homebase/index.html', context)
