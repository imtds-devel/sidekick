# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from homebase.models import Employees
import datetime


class PermanentShifts(models.Model):
    p_id = models.TextField(default="")


class Shifts(models.Model):
    LOCATION_CHOICES = (
        ('ma', 'Marshburn Library'),
        ('da', 'Darling Library'),
        ('st', 'Stamps Library'),
        ('sd', 'Support Desk'),
        ('rc', 'Repair Center'),
        ('md', 'MoD Desk'),
        ('ss', 'Senior Support Techs')
    )

    CHECKIN_CHOICES = (
        ('F', 'Not Checked In'),
        ('T', 'Checked In'),
        ('O', 'Out of Office'),
        ('W', 'West Campus'),
        ('E', 'East Campus'),
        ('A', 'Off Campus'),
        ('R', 'Regional Campus'),
        ('S', 'Refresh Day')
    )

    title = models.CharField(max_length=255)
    owner = models.ForeignKey(Employees, null=True, blank=True, related_name='shift_owner', on_delete=models.CASCADE)
    shift_date = models.DateField()
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    location = models.CharField(
        max_length=2,
        choices=LOCATION_CHOICES,
        default='ma'
    )
    is_open = models.BooleanField(default=False)
    checked_in = models.CharField(
        max_length=1,
        choices=CHECKIN_CHOICES,
        default='F'
    )
    google_id = models.TextField(default="")
    permanent = models.ForeignKey(PermanentShifts, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: owned by %s, in %s from %s to %s" % (self.title, self.owner, self.location,
                                                         self.shift_start, self.shift_end)



class ShiftCovers(models.Model):
    TYPE_CHOICES = (
        ('sf', 'Single Full Cover'),
        ('sp', 'Single Partial Cover'),
        ('pf', 'Permanent Full Cover'),
        ('pp', 'Permanent Partial Cover')
    )
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    poster = models.ForeignKey(Employees, related_name='shift_poster', on_delete=models.CASCADE)
    taker = models.ForeignKey(Employees, null = True, blank=True, related_name='shift_taker', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=''
    )
    sobstory = models.TextField(default="")
    post_date = models.DateField(default=datetime.date.today)
