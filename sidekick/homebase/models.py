# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Employee(models.Model):
    STANDING_CHOICES = (
        ('fr', 'Freshman'),
        ('sp', 'Sophomore'),
        ('jr', 'Junior'),
        ('sr', 'Senior'),
        ('ss', 'Super-Senior!'),
        ('st', 'Staff'),
        ('us', 'Unspecified')
    )

    netid = models.CharField(max_length=30, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    delete = models.BooleanField(default=False)
    phone = models.CharField(max_length=12)
    apuid = models.CharField(max_length=11)
    position = models.CharField(max_length=40)
    standing = models.CharField(
        max_length=2,
        choices=STANDING_CHOICES,
        default='us'
    )
    favcandy = models.CharField(max_length=30)
    birthday = models.DateField()
    aboutme = models.TextField()

class Proficiencies(models.Model):
    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    basic = models.IntegerField()
    advanced = models.IntegerField()
    field = models.IntegerField()
    printer = models.IntegerField()
    network = models.IntegerField()
    mobile = models.IntegerField()
    refresh = models.IntegerField()
    software = models.IntegerField()

class Passwords(models.Model):
    name = models.CharField(max_length=20)
    passwd = models.TextField()
    description = models.TextField()
    permission = models.IntegerField()

class Trophies(models.Model):
    giver = models.ForeignKey('Employee', related_name='trophyGiver', on_delete=models.CASCADE)
    recipient = models.ForeignKey('Employee', related_name='trophyRecipient', on_delete=models.CASCADE)
    reason = models.TextField()
    item_type = models.CharField(max_length=20)

class Announcements(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    announcer = models.ForeignKey('Employee', on_delete=models.CASCADE)
    announcement = models.TextField()
    sticky = models.BooleanField(default=False)

class Events(models.Model):
    announcer = models.ForeignKey('Employee', on_delete=models.CASCADE)
    description = models.TextField()
    eventStart = models.DateTimeField()
    eventEnd = models.DateTimeField()
    location = models.TextField()

class BrowserStats(models.Model):
    hits = models.IntegerField()
    chrome = models.IntegerField()
    safari = models.IntegerField()
    gecko = models.IntegerField()
    opera = models.IntegerField()
    edge = models.IntegerField()
    ie = models.IntegerField()

class Discipline(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey('Employee', related_name='disc_poster', on_delete=models.CASCADE)
    about = models.ForeignKey('Employee', related_name='disc_about', on_delete=models.CASCADE)
    description = models.TextField()
    val = models.DecimalField(max_digits=3, decimal_places=2)
    violation = models.CharField(max_length=15)

class EmailSubscriptions(models.Model):
    SHIFT_EMAIL_SUBSCRIPTION_CHOICES = (
        ('none', 'No Emails'),
        ('lab', 'Lab Tech Emails'),
        ('sd', 'Support Desk Emails'),
        ('rc', 'Repair Center Emails'),
        ('all', 'All Emails!')
    )
    BIO_EMAIL_SUBSCRIPTION_CHOICES = (
        ('none', 'No Emails'),
        ('lab', 'Lab Emails'), #for lead lab tech
        ('all', 'All Emails')
    )

    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    shift_sub = models.CharField(
        max_length=5, 
        choices=SHIFT_EMAIL_SUBSCRIPTION_CHOICES,
        default='lab'
    )

    bio_sub = models.CharField(
        max_length=5,
        choices = BIO_EMAIL_SUBSCRIPTION_CHOICES,
        default='none'
    )

class Subscriptions(models.Model):
    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    sub_type = models.CharField(max_length=5, default='both')
    sub_level = models.CharField(max_length=5, default='none')
    delete = models.BooleanField(default=False)

class FailBoard(models.Model):
    FAIL_CATEGORIES = (
        ('bs', 'Most Bad Sectors'),
        ('mj', 'Most Journals'),
        ('bn', 'Most Bad News Deliveries'),
        ('cc', 'Largest cCleaner Total Size Removed'),
        ('db', 'Longest Backup Time'),
        ('st', 'Strangest Error'),
        ('mv', 'Most Viruses'),
        ('mf', 'Worst MoD Fail'),
        ('ld', 'Longest Defrag'),
        ('bc', 'Best Comment'),
        ('lv', 'Longest Virus Scan')
    )

    fail_holder = models.ForeignKey('Employee', on_delete=models.CASCADE)
    fail_type = models.CharField(max_length=30,choices=FAIL_CATEGORIES)
    fail_val = models.CharField(max_length=20)
    date = models.DateField()

class MessageFromThePast(models.Model):
    message = models.TextField()
    posted = models.DateField(auto_now_add=True)

class ServicePrices(models.Model):
    service = models.CharField(max_length=30)
    price = models.IntegerField()
    inuse = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    placement_order = models.IntegerField()

class Shifts(models.Model):
    LOCATION_CHOICES = (
        ('ma', 'Marshburn Library'),
        ('da', 'Darling Library'),
        ('st', 'Stamps Library'),
        ('sd', 'Support Desk'),
        ('rc', 'Repair Center'),
        ('md', 'MoD Desk'),
        ('ss', 'Senior Support Tech Schedule')
    )

    title = models.CharField(max_length=255)
    owner = models.ForeignKey('Employee', related_name='shift_owner', on_delete=models.CASCADE)
    coverFor = models.ForeignKey('Employee', related_name='cover_for', on_delete=models.CASCADE)
    shift_date = models.DateField()
    shiftStart = models.DateTimeField()
    shiftEnd = models.DateTimeField()
    location = models.CharField(
        max_length=2,
        choices=LOCATION_CHOICES
    )
    is_open = models.BooleanField(default=False)
    sobstory = models.TextField()
    google_id = models.TextField()
    g_perm_id = models.TextField()

class Access(models.Model):
    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    #TODO: Define here? Or maybe modify Django's auth system?
