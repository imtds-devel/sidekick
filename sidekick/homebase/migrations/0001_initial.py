# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('announcement', models.TextField(default='')),
                ('sticky', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BrowserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hits', models.IntegerField(default=0)),
                ('chrome', models.IntegerField(default=0)),
                ('safari', models.IntegerField(default=0)),
                ('gecko', models.IntegerField(default=0)),
                ('opera', models.IntegerField(default=0)),
                ('edge', models.IntegerField(default=0)),
                ('ie', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(default='')),
                ('val', models.DecimalField(decimal_places=2, max_digits=3)),
                ('violation', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='EmailSubscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_sub', models.CharField(choices=[('no', 'No Emails'), ('lb', 'Lab Tech Emails'), ('sd', 'Support Desk Emails'), ('rc', 'Repair Center Emails'), ('al', 'All Emails!')], default='lab', max_length=2)),
                ('bio_sub', models.CharField(choices=[('no', 'No Emails'), ('lb', 'Lab Emails'), ('al', 'All Emails')], default='none', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('netid', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('fname', models.CharField(default='', max_length=30)),
                ('lname', models.CharField(default='', max_length=30)),
                ('delete', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, default='', max_length=12, null=True)),
                ('apuid', models.CharField(default='', max_length=11)),
                ('codename', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('position', models.CharField(choices=[('lbt', 'Lab Technician'), ('spt', 'Support Tech'), ('sst', 'Senior Support Tech'), ('llt', 'Lead Lab Tech'), ('mgr', 'Manager'), ('stt', 'Staff Tech'), ('stm', 'Staff Manager')], default='lbt', max_length=40)),
                ('position_desc', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('standing', models.CharField(choices=[('fr', 'Freshman'), ('sp', 'Sophomore'), ('jr', 'Junior'), ('sr', 'Senior'), ('ss', 'Super-Senior!'), ('st', 'Staff'), ('us', 'Unspecified')], default='us', max_length=2)),
                ('favcandy', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('aboutme', models.TextField(blank=True, default='', null=True)),
                ('developer', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30)),
                ('description', models.TextField(default='')),
                ('event_start', models.DateTimeField()),
                ('event_end', models.DateTimeField()),
                ('location', models.TextField(default='')),
                ('announcer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='FailBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fail_type', models.CharField(choices=[('bs', 'Most Bad Sectors'), ('mj', 'Most Journals'), ('bn', 'Most Bad News Deliveries'), ('cc', 'Largest cCleaner Total Size Removed'), ('db', 'Longest Backup Time'), ('st', 'Strangest Error'), ('mv', 'Most Viruses'), ('mf', 'Worst MoD Fail'), ('ld', 'Longest Defrag'), ('bc', 'Best Comment'), ('lv', 'Longest Virus Scan')], max_length=30)),
                ('fail_val', models.CharField(default='', max_length=20)),
                ('date', models.DateField()),
                ('fail_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='MessageFromThePast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('posted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passwords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('passwd', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('permission', models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Proficiencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.IntegerField(default=0)),
                ('advanced', models.IntegerField(default=0)),
                ('field', models.IntegerField(default=0)),
                ('printer', models.IntegerField(default=0)),
                ('network', models.IntegerField(default=0)),
                ('mobile', models.IntegerField(default=0)),
                ('refresh', models.IntegerField(default=0)),
                ('software', models.IntegerField(default=0)),
                ('netid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('shift_date', models.DateField()),
                ('shift_start', models.DateTimeField()),
                ('shift_end', models.DateTimeField()),
                ('location', models.CharField(choices=[('ma', 'Marshburn Library'), ('da', 'Darling Library'), ('st', 'Stamps Library'), ('sd', 'Support Desk'), ('rc', 'Repair Center'), ('md', 'MoD Desk'), ('ss', 'Senior Support Tech Schedule')], default='ma', max_length=2)),
                ('is_open', models.BooleanField(default=False)),
                ('checked_in', models.BooleanField(default=False)),
                ('sobstory', models.TextField(default='')),
                ('google_id', models.TextField(default='')),
                ('g_perm_id', models.TextField(default='')),
                ('coverFor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cover_for', to='homebase.Employees')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shift_owner', to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type', models.CharField(default='both', max_length=5)),
                ('sub_level', models.CharField(default='none', max_length=5)),
                ('delete', models.BooleanField(default=False)),
                ('netid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees')),
            ],
        ),
        migrations.AddField(
            model_name='emailsubscriptions',
            name='netid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees'),
        ),
        migrations.AddField(
            model_name='discipline',
            name='about',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disc_about', to='homebase.Employees'),
        ),
        migrations.AddField(
            model_name='discipline',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disc_poster', to='homebase.Employees'),
        ),
        migrations.AddField(
            model_name='announcements',
            name='announcer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees'),
        ),
        migrations.AddField(
            model_name='access',
            name='netid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees'),
        ),
    ]