# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


def index(request):
<<<<<<< HEAD
    return render(request, 'fun.html')
=======
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
>>>>>>> ALL THE THINGS, but really its just a bunch of urls, views, and the beginnings of the templating structure.
