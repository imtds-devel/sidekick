# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-17 00:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printinfo', '0002_auto_20171011_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 16, 16, 1, 5), verbose_name='Date'),
        ),
    ]
