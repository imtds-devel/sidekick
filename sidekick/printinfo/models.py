# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import datetime

# Create your models here.

STATUS_CHOICES = (
    ('healthy', 'All Good'),
    ('warning', 'Alert!'),
    ('down', 'Printer Down!')
)

class Location(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Printer(models.Model):
    printer_name = models.CharField(max_length=15, default='')          # printer name (external)
    location = models.ForeignKey(Location)                              # location of library printer dwells
    print_ip = models.URLField(max_length=14)                           # printer IP address
    print_type = models.CharField(max_length=10)                        # type of printer
    img_url = models.URLField()                                         # image of printer
    @property
    def data_targ(self):
        """Returns the netid with a #, for use with data targeting"""
        return "#%s" % self.pk
    @property
    def pic(self):
        """Returns the file path"""
        return "printers/%s_healthy.gif" % self.printer_name

    def __str__(self):
        return str(self.location) + " " + str(self.print_type)

class StatusLog(models.Model):
    print_id = models.ForeignKey(Printer)                               # printer id in database
    date = models.DateField("Date", default=datetime.now)               # date of most recent log made
    print_stat = models.CharField(max_length=12,
                                  choices=STATUS_CHOICES,
                                  default='healthy')                    # status of printer health
    desc = models.TextField(max_length=300, default='') # brief description of what's wrong
