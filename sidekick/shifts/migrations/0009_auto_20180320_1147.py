# Generated by Django 2.0 on 2018-03-20 18:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0008_auto_20180315_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shifts',
            name='checkin_time',
            field=models.TimeField(default=datetime.datetime.utcnow, null=True),
        ),
    ]
