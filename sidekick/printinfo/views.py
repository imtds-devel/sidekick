# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from .printerform import PrintInfo
from .models import Printer

# Create your views here.
def index(request):
    if request.method == "POST":
        form = PrintInfo(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    form = Printer
    return {
        'form': form
    }