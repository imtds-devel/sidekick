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
        # Copy POST data into a mutable variable
        import copy
        data = copy.copy(request.POST)

        # In case we're not in production
        # Remove this line before production!
        request.user = views.get_current_user(request)

        data['netid'] = request.user
        form = StatusLogForm(data)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    library_list = Location.objects.all()
    printer_list = Printer.objects.all()

    print_stat = []
    for printer in printer_list:
        current_status = StatusLog.objects.filter(print_id=printer.pk).order_by('date', 'pk').reverse()[:5]
        print_stat.append((printer, current_status))

    form = StatusLogForm()
    return {
        'library_list': library_list,
        'printer_list': print_stat,
        'form': form,
    }
