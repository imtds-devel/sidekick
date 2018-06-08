# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Employees(models.Model):
    STANDING_CHOICES = (
        ('fr', 'Freshman'),
        ('sp', 'Sophomore'),
        ('jr', 'Junior'),
        ('sr', 'Senior'),
        ('ss', 'Super-Senior!'),
        ('st', 'Staff'),
        ('us', 'Unspecified')
    )

    POSITION_CHOICES = (
        ('lbt', 'Lab Technician'),
        ('spt', 'Support Tech'),
        ('sst', 'Senior Support Tech'),
        ('sdr', 'Support Desk Rep'),
        ('llt', 'Lead Lab Tech'),
        ('mgr', 'Manager'),
        ('stt', 'Staff Tech'),
        ('stm', 'Staff Manager')
    )

    netid = models.CharField(max_length=30, primary_key=True)
    fname = models.CharField(max_length=30, default="")
    lname = models.CharField(max_length=30, default="")
    delete = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, default="", blank=True, null=True)
    apuid = models.CharField(max_length=11, default="")
    codename = models.CharField(max_length=20, default="", blank=True, null=True)
    position = models.CharField(
        max_length=40,
        default='lbt',
        choices=POSITION_CHOICES
    )
    position_desc = models.CharField(max_length=50, default="", blank=True, null=True)
    standing = models.CharField(
        max_length=2,
        choices=STANDING_CHOICES,
        default='us'
    )
    favcandy = models.CharField(max_length=30, default="", blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    aboutme = models.TextField(default="", null=True, blank=True)
    notify_level = models.IntegerField(default=2)
    developer = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Returns employee's full name"""
        return "%s %s" % (self.fname, self.lname)

    @property
    def short_desc(self):
        return str(self.codename) if self.codename else self.nice_position

    @property
    def nice_phone(self):
        """Return a phone number in (XXX) XXX-XXXX format"""
        if not self.phone or not str(self.phone):
            return "Number Unknown"

        return "(%s) %s-%s" % (self.phone[0:3], self.phone[4:7], self.phone[8:12])

    @property
    def nice_standing(self):
        """Format employee's standing nicely"""
        return dict(self.STANDING_CHOICES)[str(self.standing)]

    @property
    def nice_position(self):
        """Format an employee's position nicely"""
        if not self.position_desc or not str(self.position_desc):
            out = dict(self.POSITION_CHOICES)[str(self.position)]
        else:
            out = str(self.position_desc)
        return out

    @property
    def data_target(self):
        """Returns the netid with a #, for use with data targeting"""
        return "#%s" % self.netid

    @property
    def picture(self):
        """Returns the file path"""
        return "employees/%s.gif" % self.netid

    @property
    def search(self):
        out = "%s%s%s%s%s".lower() % (self.fname, self.netid, self.nice_standing, self.nice_position, self.position)
        return out.lower()


class NotifySources(models.Model):
    SOURCE_CHOICES = (
        ('e', 'email'),
        ('s', 'Slack'),
        ('t', 'Text Message')
    )

    netid = models.ForeignKey(Employees, on_delete=models.CASCADE)
    source = models.CharField(max_length=1, choices=SOURCE_CHOICES, default='e')
    details = models.TextField(default="")


class Announcements(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    announcer = models.ForeignKey(Employees, on_delete=models.CASCADE)
    subject = models.TextField(default="")
    body = models.TextField(default="")
    sticky = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subject)


class Events(models.Model):
    announcer = models.ForeignKey(Employees, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    event_date = models.DateField()
    location = models.TextField(default="")

    def __str__(self):
        return "%s: on %s" % (self.title, self.event_date)


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

    fail_holder = models.ForeignKey(Employees, on_delete=models.CASCADE)
    fail_type = models.CharField(max_length=30, choices=FAIL_CATEGORIES)
    fail_val = models.CharField(max_length=20, default="")
    date = models.DateField()


class MessageFromThePast(models.Model):
    message = models.TextField()
    posted = models.DateField(auto_now_add=True)


class StaffStatus(models.Model):
    STATUS_CHOICES = (
        ('i', 'In Office'),
        ('o', 'Out of Office'),
        ('e', 'East Campus'),
        ('w', 'West Campus'),
        ('f', 'Off Campus'),
        ('m', 'Meeting'),
    )

    netid = models.OneToOneField(Employees, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='o')
    description = models.CharField(max_length=20, default="")

class ModTasks(models.Model):
    task = models.TextField(default="")
    created_date = models.DateTimeField(default = timezone.now)
    poster = models.ForeignKey(Employees, related_name='taskPoster', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    completer = models.ForeignKey(Employees, related_name='taskCompleter', on_delete=models.CASCADE, null=True)