import httplib2
import os
import datetime
import pytz

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from sidekick.settings import CALENDAR_LOCATION_IDS
from shifts.models import SyncTokens, Shifts
from homebase.models import Employees
from shifts.functions.decorators import async

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'


def get_refresh_token():
    flow = client.flow_from_clientsecrets (CLIENT_SECRET_FILE, SCOPES)

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

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
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


def synchronize():
    locations = ['ma', 'da', 'st', 'sd', 'rc', 'md']
    for loc in locations:
        sync_location(loc)


@async
def sync_location(loc):
    # Build Google API service
    service = build_service()

    #Convert location to a calendar ID
    cal_id = CALENDAR_LOCATION_IDS[loc]

    # Init page token
    page_token = None

    # Figure out sync token
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


def process_events(list_results, loc):
    events = list_results.get('items', None)
    if not events:
        print("No events found for "+loc+"!")

    tz = pytz.timezone('America/Los_Angeles')
    now = tz.localize(datetime.datetime.now())
    for event in events:
        if event.get('status') == 'cancelled':
            shift_delete = Shifts.objects.filter(event_id=event['id'])
            print("Deleting "+str(shift_delete))
            shift_delete.delete()
            continue

        e_start = str(event.get('start').get('dateTime', "2015-01-01T00:00:00-07:00"))[:-6]
        # Check to make sure the shift is recent enough to be worth our time
        e_date = tz.localize(datetime.datetime.strptime(e_start, "%Y-%m-%dT%H:%M:%S"))
        if e_date < now-datetime.timedelta(days=60):  # if not within the last 60 days
            print("skipping")
            continue

        owner, is_open = get_owner_open(event['summary'])
        shift = Shifts(
            event_id=event['id'],
            title=event['summary'],
            owner=owner,
            shift_date=event['start']['dateTime'][0:10],
            shift_start=event['start']['dateTime'],
            shift_end=event['end']['dateTime'],
            location=loc,
            is_open=is_open,
            permanent_id=event['iCalUID']
        )
        print(shift)
        shift.save()


def get_owner_open(title: str):
    # split title into three strings: fname (or 'Open'), lname (or 'Shift'), and potentially '(Cover for fname lname)'
    t_split = title.split(" ", 3)

    # We have to figure out whether a shift is open and who owns it by using the event title!
    # If this isn't an open shift
    if t_split[0].lower() != "open":
        emps = Employees.objects.filter(fname__iexact=t_split[0], lname__iexact=t_split[1])
        is_open = False
    else:
        is_open = True
        if len(t_split) > 2:
            try:
                t_split = t_split[2].split(" ")
                f_name = t_split[2]
                l_name = t_split[3].replace(")", "")
                emps = Employees.objects.filter(fname__iexact=f_name, lname__iexact=l_name)
            except IndexError: # Because of a glitch, some owned open shifts don't have names associated with them...
                return None, True
        else:
            # This was an unowned open shift, so no owner
            return None, True

    if len(emps) > 0:
        # We'll need to do this differently if we ever get two people with the same name working for us
        return emps.first(), is_open
    else:
        return None, False
