# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from homebase.models import Employees
import datetime
import pytz


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

    event_id = models.TextField(primary_key=True)
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
    permanent_id = models.TextField(default="")  # Same as event id for non-permanent shifts

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

    @property
    def google_single_id(self):
        date = str(self.shift_date).replace("-", "")
        time = str(pytz.utc.localize(self.shift_start))
        return self.perm_id


class ShiftCovers(models.Model):
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    poster = models.ForeignKey(Employees, related_name='shift_poster', on_delete=models.CASCADE)
    taker = models.ForeignKey(Employees, null=True, blank=True, related_name='shift_taker', on_delete=models.CASCADE)
    sobstory = models.TextField(default="")
    post_date = models.DateField(default=datetime.date.today)

    @property
    def is_taken(self):
        return self.taker is None

    def __str__(self):
        if self.taker:
            return "Cover for %s was posted on %s and taken by %s" % (str(self.poster), str(self.post_date), str(self.taker))
        else:
            return "Cover for %s was posted on %s and is OPEN!" % (str(self.poster), str(self.post_date))


class SyncTokens(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=2)
    token = models.TextField(default="")
