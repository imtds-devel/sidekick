# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views

# Create your views here.
def index(request):
    context = {}
    return views.load_page(request, 'passwords/index.html', context)