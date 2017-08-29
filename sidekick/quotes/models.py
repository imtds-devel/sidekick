# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class ServicePrices(models.Model):
    service = models.CharField(max_length=30, default="")
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=20, default="")
    in_use = models.BooleanField(default=True)
    description = models.CharField(max_length=255)
    placement_order = models.IntegerField(default=0)
