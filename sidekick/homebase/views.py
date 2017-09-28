# -*- coding: utf-8 -*-
from sidekick import views
from django.contrib.auth.decorators import login_required

# @login_required
def index(request):
    context = {}
    return views.load_page(request, 'homebase/index.html', context)
