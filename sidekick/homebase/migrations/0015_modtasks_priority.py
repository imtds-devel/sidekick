# Generated by Django 2.0 on 2018-06-28 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0014_modnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='modtasks',
            name='priority',
            field=models.BooleanField(default=False),
        ),
    ]
