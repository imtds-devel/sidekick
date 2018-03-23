from django.core.mail import send_mail
from homebase.models import Employees, NotifySources

# This is a notification system for Sidekick!


# priority number meanings
# 3: Everything - Get all public notifications
# 2: Standard - Get standard array of notifications
# 1: Important - Get only private and urgent notifications

def notify(emp: Employees, subject: str, body:str):
    sources = NotifySources.objects.get(netid=emp.netid)

    for source in sources:
        if source.source == 'e':  # Email user
            send_mail(
                subject=subject,
                message=body,
                from_email="shiftmaster@sidekick.apu.edu",
                recipient_list=[str(emp.netid)+"@apu.edu"],
                fail_silently=True
            )
        elif source.source == 's':  # Slack msg user
            print("slack")
        elif source.source == 't':  # Text msg
            print("text")


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
                notify(emp)
            # Otherwise if the emp wants lots of notifications or they belong to the group
            elif emp.notify_level == 3 or (emp.position == self.position and emp.notify_level != 1):
                notify(emp)


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
        notify(self.recipient)
