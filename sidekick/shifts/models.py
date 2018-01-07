# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from homebase.models import Employees
import datetime
import pytz
from django.utils.timezone import make_aware, make_naive


class Shifts(models.Model):
    LOCATION_CHOICES = (
        ('ma', 'Marshburn'),
        ('da', 'Darling'),
        ('st', 'Stamps'),
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
    sob_story = models.TextField(null=True, blank=True) # The current sob story for the shift, can be null if the shift isn't open
    delete = models.BooleanField(default=False) # Shifts can be deleted in the case of partial shifts, but we still need to be able to reference them 

    def __str__(self):
        return "%s: owned by %s, in %s from %s to %s" % (self.title, self.owner, self.location,
                                                         self.shift_start, self.shift_end)

    @property
    def pretty_location(self):
        return[l[1] for l in self.LOCATION_CHOICES if l[0] == self.location][0]

    @property
    def short_title(self):
        return "Open Shift" if self.is_open else self.owner

    @property
    def pretty_duration(self):
        return self.shift_start.strftime("%I:%M%p")+"-"+self.shift_end.strftime("%I:%M%p")

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

    # TODO: Get this finished and experiment w/ using as replacement for single ID storage
    @property
    def google_single_id(self):
        date = str(self.shift_date).replace("-", "")
        time = str(pytz.utc.localize(self.shift_start))
        return self.permanent_id


class SyncTokens(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=2)
    token = models.TextField(default="")


class Holidays(models.Model):
    date = models.DateField()
    name = models.TextField()

    @property
    def exdate(self):
        return "EXDATE;VALUE=DATE:%s" % self.date.strftime("%Y%m%d")


class ShiftRecords(models.Model):
    ACTION_CHOICES = (
        ('na', 'No Action'),
        ('fpp', 'Full Permanent Post'),
        ('fsp', 'Full Single Post'),
        ('ppp', 'Partial Permanent Post'),
        ('psp', 'Partial Single Post'),
        ('fpt', 'Full Permanent Take'),
        ('fst', 'Full Single Take'),
        ('ppt', 'Parital Permanent Take'),
        ('pst', 'Partial Single Take')
    )

    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    actor = models.ForeignKey(Employees, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(
        max_length=3,
        choices=ACTION_CHOICES,
        default='na'
    )

    def __str__(self):
        return "%s did a %s on %s" % (str(self.actor), str(self.get_action_display()), str(self.timestamp))

