# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceprices',
            name='inuse',
        ),
        migrations.AddField(
            model_name='serviceprices',
            name='in_use',
            field=models.BooleanField(default=True),
        ),
    ]
