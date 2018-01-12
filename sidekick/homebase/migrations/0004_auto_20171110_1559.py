# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0003_auto_20171020_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discipline',
            name='about',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='proficiencies',
            name='netid',
        ),
        migrations.DeleteModel(
            name='ServicePrices',
        ),
        migrations.RemoveField(
            model_name='announcements',
            name='subject',
        ),
        migrations.AlterField(
            model_name='events',
            name='event_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='events',
            name='event_start',
            field=models.DateTimeField(),
        ),
        migrations.DeleteModel(
            name='Discipline',
        ),
        migrations.DeleteModel(
            name='Proficiencies',
        ),
    ]
