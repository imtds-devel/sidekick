# Generated by Django 2.0 on 2018-06-06 23:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0012_modtasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modtasks',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
