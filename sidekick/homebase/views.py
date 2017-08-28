# -*- coding: utf-8 -*-
from sidekick import views

#from .models import Employee

def index(request):
    context = {}
    return views.load_page(request, 'homebase/index.html', context)
