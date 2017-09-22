# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import datetime

# Create your models here.

class Printer(models.Model):
    printer_name = models.CharField(max_length=15, default='')          # printer name (external)
    print_ref = models.CharField(max_length=6)                        # printer reference name (internal)
    location = models.CharField(max_length=12)            # location of library printer dwells
    print_ip = models.URLField(max_length=14)                           # printer IP address
    print_type = models.CharField(max_length=10)                        # type of printer
    img_url = models.URLField()                                         # image of printer

class StatusLog(models.Model):
    print_id = models.ForeignKey(Printer)                               # printer id in database
    date = models.DateField("Date", default=datetime.now())             # date of most recent log made
    print_stat = models.CharField(max_length=12, default='healthy')     # status of printer health
    desc = models.TextField(max_length=300, default='')                 # brief description of what's wrong

class Library(models.Model):
    lib_id = models.CharField(max_length=12)
    printer = models.ManyToManyField(Printer)