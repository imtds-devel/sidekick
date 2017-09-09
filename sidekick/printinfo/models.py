# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Print(models.Model):
    PRINTER_CHOICES = (
        ('bwmar', 'B&W Marshburn'),
        ('comar', 'Color Marshburn'),
        ('smmar', 'Small BW Marshburn'),
        ('bwdar', 'B&W Darling'),
        ('codar', 'Color Darling'),
        ('bwstaup', 'B&W Stamps Upstairs'),
        ('bwstado', 'B&W Stamps Downstairs'),
        ('bwdome', 'B&W Cougar Dome'),
    )

class Status(models.Model):
    PRINTER_STATUS = (
        ('healthy', 'Fully Functional'),
        ('warning', 'Problem!'),
        ('OoS', 'Not Functional')
    )

class Library(models.Model):
    LIBRARY_LIST = (
        ('1', 'mar' 'Marshburn'),
        ('2', 'dar' 'Darling'),
        ('3', 'sta', 'Stamps'),
        ('4', 'dome', 'Cougar Dome')
    )

    printers = models.ForeignKey(Print, related_name='specificPrinter', on_delete=models.CASCADE)
    r = Report()

class Report(models.Model):
    date_made = models.DateTimeField('Most Recent Report Time')
    lib = models.CharField(library)
    status = models.CharField(health)
    rep = models.TextField(desc)


library = models.CharField(max_length=4, default='', choices=Library.LIBRARY_LIST)
# printers = models.ForeignKey(Print, related_name='specificPrinter', on_delete=models.CASCADE)
desc = models.TextField(max_length=140, default="")
health = models.CharField(max_length=1,
                          default='',
                          choices=Status.PRINTER_STATUS
                          )