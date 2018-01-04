# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from homebase.models import Employees
import datetime

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
    name = models.CharField(max_length=15, default='')                                       # printer name (external)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)                                 # location of library printer dwells
    print_ip = models.URLField(max_length=14)                                                        # printer IP address
    type = models.CharField(max_length=10)                                                     # type of printer
    @property
    def data_targ(self):
        """data targeted for modals"""
        return "#%s" % self.pk

    def __str__(self):
        """formatted string for printer Location and Print Type"""
        return str(self.location) + " " + str(self.type)


class StatusLog(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)                                   # printer id in database
    date = models.DateTimeField("Date", default=timezone.now)                                        # date of most recent log made
    print_stat = models.CharField(max_length=12,
                                  choices=STATUS_CHOICES)                                            # status of printer health
    desc = models.TextField(max_length=300, default='')                                              # brief description of what's wrong
    netid = models.ForeignKey(Employees, default='bduggan14', on_delete=models.CASCADE)              # Need to add model for userID to record on each form

    @property
    def pic(self):
        """Returns the picture formatted to be referenced"""
        return "printers/%s_%s.gif" % (self.printer.pk, self.print_stat)
