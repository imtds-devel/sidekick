# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

printerip = models.CharField(max_length=12)         # printer IP address
desc = models.TextField(max_length=300, default="") # short status description

# Types of Printers in the Libraries
class Print(models.Model):
    PRINTER_CHOICES = (
        ('larbw', 'Large B&W'),
        ('larco', 'Large Color'),
        ('smabw', 'Small BW'),
    )

# Different Status Options of Each Printer
class Status(models.Model):
    PRINTER_STATUS = (
        ('h', 'Fully Functional'),  # printer is healthy
        ('w', 'Problem!'),          # printer has a warning
        ('x', 'Not Functional')     # printer is down
    )

# Each Location - ranked busiest to least
class Library(models.Model):
    LIBRARY_LIST = (
        ('1', 'mar' 'Marshburn'),
        ('2', 'dar' 'Darling'),
        ('3', 'sta', 'Stamps'),
        ('4', 'dome', 'Cougar Dome')
    )

health = models.CharField(max_length=1,
                          default='',
                          choices=Status.PRINTER_STATUS
                          )

# Report Log Idea
class Report(models.Model):
    date_made = models.DateTimeField('Most Recent Report Time')
    lib = Library()
    status = Status()
    rep = models.TextField(desc)

printers = models.ForeignKey(Print, related_name='specificPrinter', on_delete=models.CASCADE)