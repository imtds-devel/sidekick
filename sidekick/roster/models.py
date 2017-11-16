# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from homebase.models import Employees


# Create your models here.

class Trophies(models.Model):
    TROPHY_TYPES = (
        # ('mil', 'Milestone'),
        ('bdg', 'Badge'),
        # ('udb', 'Under the Bus'),
        ('str', 'Star'),
        # ('hst', 'Half-Star'),
        # ('mas', 'Mastery'),
        # ('pst', 'Puzzle Star')
    )

    giver = models.ForeignKey(Employees, related_name='trophyGiver', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Employees, related_name='trophyRecipient', on_delete=models.CASCADE)
    reason = models.TextField(default="")
    name = models.TextField(default="")
    trophy_type = models.CharField(
        max_length=3,
        default="",
        choices=TROPHY_TYPES
    )
    icon = models.CharField(max_length=30, default="")

    def __str__(self):
        return "giver: " + str(self.giver) + ", recipient: " + str(self.recipient) + ", type: " + str(self.trophy_type)

    @property
    def url(self):
        if self.trophy_type == 'bdg':
            out = self.giver.netid
        elif self.trophy_type == 'str':
            if self.giver == self.recipient:
                out = 'grey-star'
            else:
                out = 'gold-star'
        else:
            out = 'grey-star'

        return "trophies/%s.gif" % out


class Discipline(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(Employees, related_name='disc_poster', on_delete=models.CASCADE)
    about = models.ForeignKey(Employees, related_name='disc_about', on_delete=models.CASCADE)
    description = models.TextField(default="")
    val = models.DecimalField(max_digits=3, decimal_places=2)
    violation = models.CharField(max_length=15, default="")

    def __str__(self):
        return "For: %s, Reason: %s, Val: %s" % (self.about, self.description, self.val)


class Proficiencies(models.Model):
    netid = models.ForeignKey(Employees, on_delete=models.CASCADE)
    basic = models.IntegerField(default=0)
    advanced = models.IntegerField(default=0)
    field = models.IntegerField(default=0)
    printer = models.IntegerField(default=0)
    network = models.IntegerField(default=0)
    mobile = models.IntegerField(default=0)
    refresh = models.IntegerField(default=0)
    software = models.IntegerField(default=0)

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % \
               (self.basic,
                self.advanced,
                self.field,
                self.printer,
                self.network,
                self.mobile,
                self.refresh,
                self.software)

    @property
    def get_as_list(self):
        return [
            self.basic,
            self.advanced,
            self.field,
            self.printer,
            self.network,
            self.mobile,
            self.refresh
        ]
