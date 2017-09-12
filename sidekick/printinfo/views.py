# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from sidekick import views
from .printerform import PrintInfo
from .models import Library

# Create your views here.
def index(request):
    if request.method == "POST":
        form = PrintInfo(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'printinfo/index.html', prep_context())

def prep_context():
    library_list = Library.objects.all().order_by('libid')
    form = PrintInfo()
    return {
        'form': form
    }