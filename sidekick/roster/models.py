# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from homebase.models import Employee


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

    giver = models.ForeignKey(Employee, related_name='trophyGiver', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Employee, related_name='trophyRecipient', on_delete=models.CASCADE)
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
