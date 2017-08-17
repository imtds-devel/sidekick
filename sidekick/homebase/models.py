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

    POSITION_CHOICES = (
        ('lbt', 'Lab Technician'),
        ('spt', 'Support Tech'),
        ('sst', 'Senior Support Tech'),
        ('llt', 'Lead Lab Tech'),
        ('mgr', 'Manager'),
        ('stt', 'Staff Tech'),
        ('stm', 'Staff Manager')
    )

    netid = models.CharField(max_length=30, primary_key=True)
    fname = models.CharField(max_length=30, default="")
    lname = models.CharField(max_length=30, default="")
    delete = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, default="")
    apuid = models.CharField(max_length=11, default="")
    codename = models.CharField(max_length=20, default="")
    position = models.CharField(
        max_length=40,
        default='lbt',
        choices=POSITION_CHOICES
    )
    position_desc = models.TextField(default="")
    standing = models.CharField(
        max_length=2,
        choices=STANDING_CHOICES,
        default='us'
    )
    favcandy = models.CharField(max_length=30, default="")
    birthday = models.DateField()
    aboutme = models.TextField(default="")
    developer = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + " " + self.lname + " (" + self.netid + ")"

    @property
    def full_name(self):
        """Returns employee's full name"""
        return "%s %s" % (self.fname, self.lname)

    @property
    def short_desc(self):
        c_name = str(self.codename)
        return c_name if c_name else str(self.nice_position)

    @property
    def nice_phone(self):
        """Return a phone number in (XXX) XXX-XXXX format"""
        return "(%s) %s-%s" % (self.phone[0:3], self.phone[4:7], self.phone[8:12])

    @property
    def nice_standing(self):
        """Format employee's standing nicely"""
        return dict(self.STANDING_CHOICES)[str(self.standing)]

    @property
    def nice_position(self):
        """Format an employee's position nicely"""
        return dict(self.POSITION_CHOICES)[str(self.position)] if not str(self.position_desc) else str(self.position_desc)

    @property 
    def data_target(self):
        """Returns the netid with a #, for use with data targeting"""
        return "#%s" % self.netid
    
    @property
    def picture(self):
        """Returns the file path"""
        return "employees/%s.gif" % self.netid


class Proficiencies(models.Model):
    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    basic = models.IntegerField(default=0)
    advanced = models.IntegerField(default=0)
    field = models.IntegerField(default=0)
    printer = models.IntegerField(default=0)
    network = models.IntegerField(default=0)
    mobile = models.IntegerField(default=0)
    refresh = models.IntegerField(default=0)
    software = models.IntegerField(default=0)

    def __str__(self):
        return "%s(%s, %s, %s, %s, %s, %s, %s)" % \
               (self.netid,
                self.basic,
                self.advanced,
                self.field,
                self.printer,
                self.network,
                self.mobile,
                self.refresh)

    @property
    def get_as_list(self):
        return [
            self.basic,
            self.advanced,
            self.field,
            self.printer,
            self.network,
            self.mobile,
            self.refresh
        ]


class Passwords(models.Model):
    name = models.CharField(max_length=20, default="")
    passwd = models.TextField(default="")
    description = models.TextField(default="")
    permission = models.IntegerField(default=3)

    def __str__(self):
        return self.name + ": " + self.description


class Announcements(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    announcer = models.ForeignKey('Employee', on_delete=models.CASCADE)
    announcement = models.TextField(default="")
    sticky = models.BooleanField(default=False)

    def __str__(self):
        return str(self.announcement)


class Events(models.Model):
    announcer = models.ForeignKey('Employee', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    location = models.TextField(default="")

    def __str__(self):
        return "%s: from %s to %s" % (self.title, self.event_start, self.event_end)


class BrowserStats(models.Model):
    hits = models.IntegerField(default=0)
    chrome = models.IntegerField(default=0)
    safari = models.IntegerField(default=0)
    gecko = models.IntegerField(default=0)
    opera = models.IntegerField(default=0)
    edge = models.IntegerField(default=0)
    ie = models.IntegerField(default=0)

    def __str__(self):
        return "Hits: %s (%s chrome, %s safari, %s firefox, %s opera, %s edge, %s ie)" % (
            self.hits,
            self.chrome,
            self.safari,
            self.gecko,
            self.opera,
            self.edge,
            self.ie
        )


class Discipline(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey('Employee', related_name='disc_poster', on_delete=models.CASCADE)
    about = models.ForeignKey('Employee', related_name='disc_about', on_delete=models.CASCADE)
    description = models.TextField(default="")
    val = models.DecimalField(max_digits=3, decimal_places=2)
    violation = models.CharField(max_length=15, default="")

    def __str__(self):
        return "For: %s, Reason: %s, Val: %s" % (self.about, self.description, self.val)


class EmailSubscriptions(models.Model):
    SHIFT_EMAIL_SUBSCRIPTION_CHOICES = (
        ('no', 'No Emails'),
        ('lb', 'Lab Tech Emails'),
        ('sd', 'Support Desk Emails'),
        ('rc', 'Repair Center Emails'),
        ('al', 'All Emails!')
    )
    BIO_EMAIL_SUBSCRIPTION_CHOICES = (
        ('no', 'No Emails'),
        ('lb', 'Lab Emails'),  # for lead lab tech
        ('al', 'All Emails')
    )

    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    shift_sub = models.CharField(
        max_length=2,
        choices=SHIFT_EMAIL_SUBSCRIPTION_CHOICES,
        default='lab'
    )

    bio_sub = models.CharField(
        max_length=2,
        choices=BIO_EMAIL_SUBSCRIPTION_CHOICES,
        default='none'
    )

    def __str__(self):
        return "%s: shift=%s, bio=%s" % (self.netid, self.shift_sub, self.bio_sub)


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
    fail_type = models.CharField(max_length=30, choices=FAIL_CATEGORIES)
    fail_val = models.CharField(max_length=20, default="")
    date = models.DateField()


class MessageFromThePast(models.Model):
    message = models.TextField()
    posted = models.DateField(auto_now_add=True)


class ServicePrices(models.Model):
    service = models.CharField(max_length=30, default="")
    price = models.IntegerField(default=0)
    inuse = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    placement_order = models.IntegerField(default=0)


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
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    location = models.CharField(
        max_length=2,
        choices=LOCATION_CHOICES,
        default='ma'
    )
    is_open = models.BooleanField(default=False)
    sobstory = models.TextField(default="")
    google_id = models.TextField(default="")
    g_perm_id = models.TextField(default="")

    def __str__(self):
        return "%s: owned by %s, in %s from %s to %s" % (self.title, self.owner, self.location,
                                                         self.shift_start, self.shift_end)


class Access(models.Model):
    netid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    # TODO: Define here? Or maybe modify Django's auth system?
