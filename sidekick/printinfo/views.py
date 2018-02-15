# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Printer
from .models import Location
from .models import StatusLog
from django.http import HttpResponse, HttpResponseRedirect
from sidekick import views
from .forms import StatusLogForm
from django.http import JsonResponse

# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":
        # Copy POST data into a mutable variable
        import copy
        data = copy.copy(request.POST)

        # In case we're not in production
        # Remove this line before production!
        request = views.get_current_user(request)

        data['netid'] = request.user
        form = StatusLogForm(data)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def get_reports(request):
    printpk = request.GET.get('printpk', None)

    reports = StatusLog.objects.filter(printer_id=printpk)

    # Construct query of comments according to each printpk
    translated_reports = [{
        'pk': report.printer.pk,
        'netid': report.netid_id,
        'print_stat': report.print_stat,
        'date': report.date.strftime("%m/%d/%y"),
        'desc': report.desc
    } for report in reports]

    data = {
        'replist': list(translated_reports)
    }
    print()

    return JsonResponse(data)


def prep_context():
    library_list = Location.objects.all()
    printer_list = Printer.objects.all()

    print_stat = []
    for printer in printer_list:
        current_status = StatusLog.objects.filter(printer=printer.pk).order_by('date', 'pk').reverse()[:5]
        print_stat.append((printer, current_status))

    form = StatusLogForm()
    return {
        'library_list': library_list,
        'printer_list': print_stat,
        'form': form,
    }
