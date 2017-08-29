# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sidekick import views
from .models import ServicePrices

# Create your views here.
def index(request):
    services_list = ServicePrices.objects.all().order_by('placement_order')
    context={'services_list': services_list}
    return views.load_page(request, 'quotes/index.html', context)