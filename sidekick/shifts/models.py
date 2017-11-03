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
        ('sr', 'Support Reps'),
        ('rc', 'Repair Center'),
        ('md', 'MoD Desk'),
        ('ss', 'Senior Support Techs'),
        ('sf', 'Staff'),
        ('te', 'TESTING')
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
    shift_start = models.TimeField()
    shift_end = models.TimeField()
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

    @property
    def google_start(self):
        return "%sT%s" % (str(self.shift_date), str(self.shift_start))

    @property
    def google_end(self):
        date = self.shift_date

        # If the shift starts before midnight and ends after midnight, we need to increment the date
        # Note: if shifts ever extend past 1am, this will need to be updated
        if int(self.shift_start.hour) > 2 > int(self.shift_end.hour):
            date += datetime.timedelta(days=1)

        return "%sT%s" % (str(date), str(self.shift_start))


class ShiftCovers(models.Model):
    TYPE_CHOICES = (
        ('sf', 'Single Full Cover'),
        ('sp', 'Single Partial Cover'),
        ('pf', 'Permanent Full Cover'),
        ('pp', 'Permanent Partial Cover')
    )
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    poster = models.ForeignKey(Employees, related_name='shift_poster', on_delete=models.CASCADE)
    taker = models.ForeignKey(Employees, null=True, blank=True, related_name='shift_taker', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=''
    )
    sobstory = models.TextField(default="")
    post_date = models.DateField(default=datetime.date.today)
    permanent = models.BooleanField(default=False)

    @property
    def is_taken(self):
        return self.taker is None

    # Modify properties of shift that are common to all shift takes
    # NOTE: This will NOT modify the time of the shift!
    def take(self, taker: Employees):
        self.taker = taker
        self.shift.is_open = False
        old_owner = str(self.shift.owner)
        self.shift.owner = taker
        self.shift.description = str(taker) + " (cover for " + old_owner + ")"

    def __str__(self):
        if self.taker:
            return "Cover for %s was posted on %s and taken by %s" % (str(self.poster), str(self.post_date), str(self.taker))
        else:
            return "Cover for %s was posted on %s and is OPEN!" % (str(self.poster), str(self.post_date))


class Tokens(models.Model):
    refresh_token = models.TextField(default="")
    access_token = models.TextField(default="")
