# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homebase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trophies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(default='')),
                ('name', models.TextField(default='')),
                ('trophy_type', models.CharField(choices=[('mil', 'Milestone'), ('bdg', 'Badge'), ('udb', 'Under the Bus'), ('str', 'Star'), ('hst', 'Half-Star'), ('mas', 'Mastery'), ('pst', 'Puzzle Star')], default='', max_length=3)),
                ('icon', models.CharField(default='', max_length=30)),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trophyGiver', to='homebase.Employee')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trophyRecipient', to='homebase.Employee')),
            ],
        ),
    ]
