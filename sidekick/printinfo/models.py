# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import datetime
from homebase.models import Employees

# Create your models here.

STATUS_CHOICES = (
    ('healthy', 'All Good'),
    ('warning', 'Alert!'),
    ('down', 'Printer Down!')
)

class Location(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        """Returns the reference of the Location Name"""
        return self.name

class Printer(models.Model):
    printer_name = models.CharField(max_length=15, default='')                                       # printer name (external)
    location = models.ForeignKey(Location)                                                           # location of library printer dwells
    print_ip = models.URLField(max_length=14)                                                        # printer IP address
    print_type = models.CharField(max_length=10)                                                     # type of printer
    @property
    def data_targ(self):
        """data targeted for modals"""
        return "#%s" % self.pk

    def __str__(self):
        """formatted string for printer Location and Print Type"""
        return str(self.location) + " " + str(self.print_type)

class StatusLog(models.Model):
    print_id = models.ForeignKey(Printer)                                                            # printer id in database
    date = models.DateTimeField("Date", default=datetime.now().replace(microsecond=0))               # date of most recent log made
    print_stat = models.CharField(max_length=12,
                                  choices=STATUS_CHOICES)                                            # status of printer health
    desc = models.TextField(max_length=300, default='')                                              # brief description of what's wrong
    netid = models.ForeignKey(Employees, default='bduggan14')                                        # Need to add model for userID to record on each form
    @property
    def pic(self):
        """Returns the picture formated to be referenced"""
        return "printers/%s_%s.gif" % (self.print_id.pk, self.print_stat)

