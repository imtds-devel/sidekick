from multiprocessing.dummy import Pool as Threadpool
from homebase.models import Employees, NotifySources
from shifts.models import Shifts
from sidekick.settings import HARAMBOT_NOTIFY
from django.core.mail import EmailMessage
from django.db.models import Q
from datetime import datetime
import requests
# This is a notification system for Sidekick!


# Call this function with a list of employees that should receive the message
def notify_employees(emps, subject: str, body: str):
    email_sources = []
    for emp in emps:
        # Skip if emp is None for some reason
        if not emp or emp.delete:
            continue

        sources = NotifySources.objects.filter(netid=emp.netid)
        for source in sources:
            if source.source == 's':
                # Notify via slack message
                msg_body = {subject: body}

                url = HARAMBOT_NOTIFY + "%40" + str(source.details)

                r = requests.post(url=url, data=msg_body, json=True)

                # TODO: Verify status and log on failure
            elif source.source == 't':
                number = ''.join(i for i in emp.phone if i.isdigit())
                email_sources.append(str(number)+"@"+source.details)
            elif source.source == 'e':
                email_sources.append(str(emp.netid)+"@apu.edu")

    # Send group email to all recipients
    EmailMessage(
        subject=subject,
        body=body,
        from_email="Sidekick Webmaster <webmaster@sidekick.apu.edu>",
        bcc=email_sources
    ).send()
    return True


# Notify all MoDs and staff members
def notify_manager_team(subject: str, body: str):
    emps = Employees.objects.filter(
        Q(position='mgr') | Q(position='stm')
    ).filter(notify_level__gte=2, delete=False)
    return notify_employees(emps, subject, body)


# Notify all MoDs in a specific time range
def notify_mods_in_range(subject: str, body: str, start: datetime, end: datetime):
    shifts = Shifts.objects.filter(
        Q(shift_start__lt=end, shift_end__gte=end) | Q(shift_end__gt=start, shift_start__lte=start)
    ).filter(location='mod').exclude(owner__isnull=True, owner__exact='')  # filter empty owners

    if len(shifts) == 0:
        # Notify night MoD for night shifts
        shifts = [
            Shifts.objects.filter(
                shift_end__lte=start
            ).first()
        ]

    emps = list(set([shift.owner for shift in shifts]))  # Convert to a set to eliminate potential duplicates

    # return notify_employees(emps, subject, body)
    return emps


# Notify a specific employee
def notify_employee(subject: str, body: str, emp: Employees):
    return notify_employees([emp], subject, body)


# Notify all employees of a specific position
def notify_position(subject: str, body: str, position: str):
    if position == "lbt":
        # notify the lead lab techs too for lab tech things
        emps = Employees.objects.filter(Q(position=position, notify_level__gte=2) | Q(position='llt') | Q(notify_level=3)).filter(delete=False)
    else:
        emps = Employees.objects.filter(Q(position=position, notify_level__gte=2) | Q(notify_level=3)).filter(delete=False)

    return notify_employees(emps, subject, body)


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
