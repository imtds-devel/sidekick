import httplib2
import os
<<<<<<< HEAD
import datetime
import pytz
=======
>>>>>>> develop

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

<<<<<<< HEAD
from sidekick.settings import CALENDAR_LOCATION_IDS
from shifts.models import SyncTokens, Shifts
from homebase.models import Employees
from shifts.functions.decorators import async
=======
>>>>>>> develop

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'


def get_refresh_token():
<<<<<<< HEAD
    flow = client.flow_from_clientsecrets (CLIENT_SECRET_FILE, SCOPES)
=======
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
>>>>>>> develop

    storage = Storage("store-oauth2.json")
    args = tools.argparser.parse_args([])
    args.noauth_local_webserver = True
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, args)

    return credentials.refresh_token


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    flags = tools.argparser.parse_args([])

<<<<<<< HEAD
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
=======
    credential_dir = "/var/www/html/.credentials"
>>>>>>> develop
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
<<<<<<< HEAD
=======

>>>>>>> develop
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def build_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)


<<<<<<< HEAD
def synchronize(flush: bool):
    if flush:
        print("FLUSHING DATABASE NOW")
        Shifts.objects.all().delete()
        SyncTokens.objects.all().delete()

    # one for each calendar location
    locations = ['ma', 'da', 'st', 'sd', 'rc', 'md']
    for loc in locations:
        sync_location(loc)


# This is an asynchronous function that runs in its own thread, meaning we can synchronize in the background!
# It uses the async decorator, which we declare in decorators.py
@async
def sync_location(loc):
    # Build Google API service
    service = build_service()

    # Convert location to a calendar ID
    cal_id = CALENDAR_LOCATION_IDS[loc]

    # Init page token
    page_token = None

    # Figure out sync token (retrieve from db or incorporate here)
    token_data = SyncTokens.objects.filter(location=loc).order_by('timestamp').first()
    if token_data is not None:
        sync_token = token_data.token
    else:
        sync_token = None

    # Loop until there's nothing left to synchronize!
    while True:

        list_results = service.events().list(
            calendarId=cal_id,
            syncToken=sync_token,
            singleEvents=True,
            pageToken=page_token
        ).execute()

        process_events(list_results, loc)

        page_token = list_results.get('nextPageToken')
        if not page_token:
            break

    # Save new sync token to database if it's changed
    if sync_token != list_results['nextSyncToken']:
        SyncTokens(
            location=loc,
            token=list_results['nextSyncToken']
        ).save()
    print(loc + ": Thread Closing Now")


# This function processes events and converts them to shifts
# We're running it asynchronously so that we don't have to wait for the API to make calls
@async
def process_events(list_results, loc):
    # First, get a list of items from the list results
    events = list_results.get('items', None)
    if not events: # If no events
        print(loc+": No events found!")

    # Declare our timezone for timezone-aware comparisons later
    tz = pytz.timezone('America/Los_Angeles')
    # Figure out when now is in our timezone
    now = tz.localize(datetime.datetime.now())
    for event in events:

        # If the event has been deleted on the cal, delete it from our db as well
        if event.get('status') == 'cancelled':
            shift_delete = Shifts.objects.filter(event_id=event['id'])
            print(loc+": Deleting "+str(shift_delete))
            shift_delete.delete()
            continue

        # Figure out when the event starts (ignore all-day events by pretending they took place 3 years ago)
        # We have to strip timezone from the dateTime because Python can't easily create a date with the timezone
        # But since we'll never be in anything other than America/Los_Angeles, that doesn't matter
        e_start = str(event.get('start').get('dateTime', "2015-01-01T00:00:00-07:00"))[:-6]

        # Check to make sure the shift is within the last 60 days, otherwise skip it
        e_date = tz.localize(datetime.datetime.strptime(e_start, "%Y-%m-%dT%H:%M:%S"))
        if e_date < now-datetime.timedelta(days=60):
            print(loc+": skipping")
            continue

        # Figure out who owns the shift and whether it's open based on the event summary
        owner, is_open = get_owner_open(event['summary'])

        # Build the shift model and save to our database
        shift = Shifts(
            event_id=event['id'],
            title=event['summary'],
            owner=owner,
            shift_date=event['start']['dateTime'][0:10],
            shift_start=event['start']['dateTime'],
            shift_end=event['end']['dateTime'],
            location=loc,
            is_open=is_open,
            permanent_id=event['iCalUID'][:-11]  # cut out the @google.com in the permanent ID
        )
        print(loc+": "+str(shift))
        shift.save()


# Use a shift's title to infer whether the shift is open and who owns it
def get_owner_open(title: str):
    # split title into three strings: fname (or 'Open'), lname (or 'Shift'), and potentially '(Cover for fname lname)'
    t_split = title.split(" ", 2)

    # We have to figure out whether a shift is open and who owns it by using the event title!
    # If this isn't an open shift
    if t_split[0].lower() != "open":
        emps = Employees.objects.filter(fname__iexact=t_split[0], lname__iexact=t_split[1])
        is_open = False
    # If this is an open shift
    else:
        is_open = True
        # This could either be a shift with no previous owner (eg a chapel shift) or a posted cover
        # If it's a cover, then there will be a "(Cover for fname lname)" type text, so we can analyze the name
        print(t_split)
        if len(t_split) > 2:
            try:
                t_split = t_split[2].split(" ")
                f_name = t_split[2]
                l_name = t_split[3].replace(")", "")
                print(f_name+" "+l_name)
                emps = Employees.objects.filter(fname__iexact=f_name, lname__iexact=l_name)
            except IndexError:  # Because of a glitch, some owned open shifts don't have names associated with them...
                return None, True
        else:
            # This was an unowned open shift, so no owner
            return None, True

    # If we found anyone, return the first employee (should only be one)
    if len(emps) > 0:
        # We'll need to do this differently if we ever get two people with the same name working for us
        return emps.first(), is_open
    else:
        return None, False
=======
>>>>>>> develop
