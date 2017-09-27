# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Printer
from .models import Location
from sidekick import views
from .printerform import PrinterForm

# Create your views here.
def index(request):

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    library_list = Location.objects.all()
    printer_list = Printer.objects.all()
    form = PrinterForm()
    return {
        'library_list': library_list,
        'printer_list': printer_list,
        'form': form
    }
