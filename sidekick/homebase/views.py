# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def passwords(request):
    return render(request, 'passwords.html')

def printinfo(request):
    return render(request, 'printinfo.html')

def quotes(request):
    return render(request, 'quotes.html')

def roster(request):
    return render(request, 'roster.html')

def shifts(request):
    return render(request, 'shifts.html')
