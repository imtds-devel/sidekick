# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Passwords(models.Model):

    name = models.CharField(max_length=20, default="")
    passwd = models.TextField(default="")
    description = models.TextField(default="")
    permission = models.IntegerField(default=3)

    def __str__(self):
        return self.name + ": " + self.description


class PassPermission(models.Model):
    PASS_PERM_OPTIONS = (
        ('lab', 'Lab Access'),
        ('sup', 'Support Access'),
        ('mgr', 'Manager Access'),
        ('dev', 'Developer Access'),
        ('all', 'All access'),
        ('non', 'No Access (hide)')
    )

    pass_id = models.ForeignKey(Passwords, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=3,
        choices=PASS_PERM_OPTIONS,
        default='non'
    )
