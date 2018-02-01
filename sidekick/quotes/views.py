# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sidekick import views
from .models import ServicePrices


# Create your views here.
def index(request):
    services_list = ServicePrices.objects.all().order_by('placement_order')
    context={'services_list': services_list}
<<<<<<< HEAD
    return views.load_page(request, 'quotes/index.html', context)
=======
    return views.load_page(request, 'quotes/index.html', context)
>>>>>>> d41c5d16ef058133bddc86709d513bf06ee0d2ca
