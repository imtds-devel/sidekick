# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views
from django.utils import timezone
from shifts.functions.push_covers import push_cover

# Create your views here.
def index(request):

    # We import the current time
    now = timezone.now()
    context = {'time': now}
    return views.load_page(request, 'shifts/index.html', context)


