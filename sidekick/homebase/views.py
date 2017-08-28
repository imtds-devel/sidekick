# -*- coding: utf-8 -*-
from sidekick import views


def index(request):
    context = {}
    return views.load_page(request, 'homebase/index.html', context)
