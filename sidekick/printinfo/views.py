# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from .models import Library
from .models import Printer
from sidekick import views
from .printerform import PrintInfo

# Create your views here.
def index(request):
    if request.method == "POST":
        form = PrintInfo(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    library_list = {
        "Marshburn":1,
        "Darling": 2,
        "Stamps": 3,
        "Dome": 4
    }
    printer_list = {
        "BW MAR": 1,
        "COLOR MAR": 1,
        "SBW MAR": 1,
        "BW DAR": 2,
        "COLOR DAR": 2,
        "UBW STA": 3,
        "DBW STA": 3,
        "SBW DOME": 4

    }
    marshburn = {
        "B&W": 1,
        "COLOR": 1,
        "B&W Mini": 1,
    }
    darling = {
        "B&W": 2,
        "COLOR": 2,
    }
    stamps = {
        "Upper B&W": 3,
        "Lower B&W": 3,
    }
    dome = {
        "B&W Mini": 4
    }
    form = PrintInfo()
    return {
        'Marshburn': marshburn,
        'Darling': darling,
        'Stamps': stamps,
        'Dome': dome,
        'library_list': Printer.location,
        'printer_list': Printer.print_type,
        'form': form
    }
