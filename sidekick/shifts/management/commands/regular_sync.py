from django.core.management.base import BaseCommand, CommandError
from shifts.functions.sync import synchronize


# This class registers a command that can be used by manage.py. In production, there is a scheduled process
# that runs this command once every five minutes.
class Command(BaseCommand):
    help = "Synchronize the database with Google Calendar"

    def handle(self, *args, **options):
        synchronize(flush=False)
