# Generated by Django 2.0 on 2018-06-08 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0016_modtasks_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modtasks',
            name='completer',
        ),
        migrations.RemoveField(
            model_name='modtasks',
            name='poster',
        ),
        migrations.DeleteModel(
            name='ModTasks',
        ),
    ]
