# Generated by Django 2.0 on 2018-06-04 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printinfo', '0005_auto_20180604_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 4, 12, 28, 42), verbose_name='Date'),
        ),
    ]
