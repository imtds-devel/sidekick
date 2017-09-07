# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Printers(models.Model):
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

library = models.CharField(max_length=30, default="")
printer = models.ForeignKey(Printers, related_name='specificPrinter', on_delete=models.CASCADE)
report = models.TextField(max_length=140, default="")
health = models.CharField(max_length=1,
                          default='',
                          choices= Status.PRINTER_STATUS
                          )
