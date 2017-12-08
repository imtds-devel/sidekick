# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Passwords(models.Model):
    name = models.CharField(max_length=20, default="")
    passwd = models.TextField(default="")
    description = models.TextField(default="")
    permission = models.IntegerField(default=3)

    def __str__(self):
        return self.name + ": " + self.description