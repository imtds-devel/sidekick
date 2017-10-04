# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Printer
from .models import Location
from .models import StatusLog
from django.http import HttpResponseRedirect
from sidekick import views
from .forms import StatusLogForm

# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":
        form = StatusLogForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    library_list = Location.objects.all()
    printer_list = Printer.objects.all()
    status_log = StatusLog.objects.all()
    form = StatusLogForm()
    return {
        'library_list': library_list,
        'printer_list': printer_list,
        'status_log': status_log,
        'form': form
    }
