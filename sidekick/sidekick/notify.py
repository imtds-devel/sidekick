from homebase.models import Employees

# This is a notification system for Sidekick!


# priority number meanings
# 3: Everything - Get all public notifications
# 2: Standard - Get standard array of notifications
# 1: Important - Get only private notifications
# 0: Urgent - Techs on the list receive notifications regardless of their subscription

def notify(emp: Employees):
    print(emp)


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


class PrivateNotification:
    def __init__(self, name: str, subject: str, body: str, urgent: bool, recipient: Employees):
        self.recipient = recipient
        self.urgent = urgent
        self.subject = subject
        self.body = body

    def __str__(self):
        return self.subject

    def send(self):
        notify(self.recipient)
