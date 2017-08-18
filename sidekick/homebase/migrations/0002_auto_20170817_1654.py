# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='aboutme',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='codename',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='favcandy',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(default='', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position_desc',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
