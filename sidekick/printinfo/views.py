# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views

# Create your views here.
def index(request):
    context = {}
    return views.load_page(request, 'printinfo/index.html', context)

def prep_context():
    printer_list = Printers.objects.all().order_by('libnum')
    form = PrinterForm()
    return {
        'printer_list': printer_list,
        'form': form
    }