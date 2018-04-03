from django.core.mail import send_mail
from homebase.models import Employees, NotifySources
from sidekick.settings import HARAMBOT_NOTIFY
import requests

# This is a notification system for Sidekick!


# priority number meanings
# 3: Everything - Get all public notifications
# 2: Standard - Get standard array of notifications
# 1: Important - Get only private and urgent notifications

def notify(emp: Employees, subject: str, body: str):
    print("Sending notify!")
    sources = NotifySources.objects.filter(netid=emp.netid)

    for source in sources:
        if source.source == 'e':  # Email user
            send_mail(
                subject=subject,
                message=body,
                from_email="Sidekick Webmaster <webmaster@sidekick.apu.edu>",
                recipient_list=[str(emp.netid)+"@apu.edu"],
                fail_silently=True
            )
        elif source.source == 's':  # Slack msg user
            msg_body = {subject: body}

            url = HARAMBOT_NOTIFY+"%40"+str(source.details)

            r = requests.post(url=url, data=msg_body, json=True)

            # TODO: Verify status and log on failure

        elif source.source == 't':  # Text msg
            send_mail(
                subject=subject,
                message=body,
                from_email="Sidekick Webmaster <webmaster@sidekick.apu.edu>",
                recipient_list=[str(emp.phone_msg)+"@"+source.details]
            )


# PublicNotifications are notifications that go out to a particular set of Device Solutions employees
# Who it goes out to is determined by the 'position' parameter, which accepts an input like 'lbt' or 'spt'
# For a complete list of positions, see the POSITION_CHOICES variable in homebase/models.py
class PublicNotification:
    def __init__(self, name: str, subject: str, body: str, urgent: bool, position: str):
        self.position = position
        self.urgent = urgent
        self.subject = subject
        self.body = body

    def __str__(self):
        return self.subject

    def send(self):
        for emp in Employees.objects.get(delete=False):
            # If urgent
            if self.urgent:
                notify(emp, self.subject, self.body)
            # Otherwise if the emp wants lots of notifications or they belong to the right group
            elif emp.notify_level == 3 or (emp.position == self.position and emp.notify_level != 1):
                notify(emp, self.subject, self.body)


# PrivateNotifications go to the employee in particular as well as to relevant MoDs.
class PrivateNotification:
    def __init__(self, subject: str, body: str, urgent: bool, discipline: bool, recipient: Employees):
        self.recipient = recipient
        self.urgent = urgent
        self.discipline = discipline
        self.subject = subject
        self.body = body

    def __str__(self):
        return self.subject

    def send(self):
        notify(self.recipient, self.subject, self.body)


CARRIER_TO_EMAIL = {
    'Verizon': 'vtext.com',
    'T-Mobile': 'tmomail.net',
    'AT&T': 'txt.att.net',
    'Sprint': 'messaging.sprintpcs.com',
    'Virgin Mobile': 'vmobl.com',
    'Metro PCS': 'mymetropcs.com',
    'Boost Mobile': 'sms.myboostmobile.com',
    'Cricket': 'sms.cricketwireless.net',
    'Republic Wireless': 'text.republicwireless.com',
    'Google Fi (Project Fi)': 'msg.fi.google.com',
    'U.S. Cellular': 'email.uscc.net',
    'Ting': 'message.ting.com',
    'Consumer Cellular': 'mailmymobile.net',
    'C-Spire': 'cspire1.com'
}
