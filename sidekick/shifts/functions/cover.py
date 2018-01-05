from django.db.models import Q
from shifts.models import Shifts
from homebase.models import Employees
from shifts.functions import google_api
from sidekick.settings import CALENDAR_LOCATION_IDS
import datetime
import pytz


# Class that details instructions for posting and taking shift covers
# Note: because this initializes a google service, it should only be created when we *know* a cover will take place
class CoverInstructions:
    def __init__(self, post, permanent, partial, shift_id, actor: Employees, start_time: datetime.datetime=None,
                 end_time: datetime.datetime=None, sob_story=""):
        self.post = post
        self.permanent = permanent
        self.partial = partial
        self.shift_id = shift_id
        self.actor = actor
        self.start_time = start_time
        self.end_time = end_time
        self.sob_story = sob_story
        self.update_params = {
            "post": None,
            # More can be defined here if necessary
        }
        self.g_service = google_api.build_service()  # build at create time

    def push(self):
        return push_cover(self)


##############################################################
# Main post/take fns
# Master routing fn (called by CoverInstructions, routes shift covers properly!)
def push_cover(data: CoverInstructions):
    return partial_cover(data) if data.partial else full_cover(data)


# For full covers of any kind
def full_cover(data: CoverInstructions):
    print('FullCover called!')
    # 1. Get all shifts associated with this cover (could be one or many)
    shifts = Shifts.objects.filter(event_id__contains=data.shift_id).order_by('shift_date')
    print([s for s in shifts])

    # 2. Save some useful attributes for later
    first = shifts.first()
    # Verify shift exists in our db
    if first is None:
        print("Shift does not exist!")
        return False

    location = first.location
    cal_id = CALENDAR_LOCATION_IDS[location]
    tz = pytz.timezone('America/Los_Angeles')

    old_event_id = first.permanent_id
    print(old_event_id)

    # Define the shift owner
    owner = first.owner if data.post else data.actor

    # Construct new title
    if data.post:
        new_title = "Open Shift (Cover for %s)" % data.actor
    else:
        new_title = "%s (Cover for %s)" % (data.actor, owner)

    # 3. Create new Google Event
    # Start by figuring out the end repeat date if necessary
    end_repeat = get_end_repeat(shifts.last().shift_date, data.permanent)

    # Construct event
    event = build_event(
        title=new_title,
        start=tz.localize(first.shift_start),
        end=tz.localize(first.shift_end),
        end_repeat=end_repeat,
        sob_story=data.sob_story
    )

    print(event)
    print(cal_id)
    # Ship it to Google
    new_event = data.g_service.events().insert(
        calendarId=cal_id,
        body=event
    ).execute()
    print(new_event)

    # Delete old event from Google
    data.g_service.events().delete(
        calendarId=cal_id,
        eventId=old_event_id
    ).execute()

    """
    # This code is completely unnecessary, but I'm saving it just in case I'm wrong about that
    # 4. Save changes to db
    # Create new shifts in db
    for shift in shifts:
        shift.title = new_title
        shift.owner = owner
        shift.is_open = True if data.post else False
        if data.permanent:
            # Individual instances of recurring events have IDs that are derivable using the start datetime of the event
            # To build the ID, we'll need the recurring ID, the shift date (formatted as yyyymmdd), and the shift time
            # (which is formatted in ThhmmssZ with the letters T and Z around the outside
            # Note that the timezone has to be UTC :/
            # Overall format : [eventId]_yyyymmddThhmmssZ
            utc_start = shift.shift_start.astimezone(pytz.utc)

            shift.event_id = str(new_event['id'])\
                + "_"+str(shift.shift_date).replace("-", "")\
                + "T"+str(utc_start.hour)+str(utc_start.minute)+"00Z"
        else:
            shift.event_id = new_event['id']

        shift.permanent_id = new_event['iCalUID'][:-11]  # prune the @google.com
        print(shift)
        shift.save()

    # delete old shifts
    old_shifts = Shifts.objects.filter(event_id__contains=data.shift_id).order_by('shift_date')
    for s in old_shifts:
        s.delete()
        print(s)
    """

    return shift_email(data)


# For partial covers of any kind
# Unfortunately, this is a good deal more complex than full covers :/
def partial_cover(data: CoverInstructions):
    # 1. Get all shifts associated with cover (could be 1 or many)
    shifts = Shifts.objects.filter(event_id__contains=data.shift_id).order_by('shift_date')

    # 2. Save some useful attributes for later
    first = shifts.first()
    # Verify shift exists in our db
    if first is None:
        print("Shift does not exist!")
        return False

    location = first.location
    cal_id = CALENDAR_LOCATION_IDS[location]
    old_event_id = first.permanent_id
    og_start = datetime.datetime(first.shift_start)
    og_end = datetime.datetime(first.shift_end)
    if not data.post:
        sob_story = first.sob_story
    else:
        sob_story = ""

    # 3. Figure out how to split shift using start and end times
    # Start by doing basic validation on start & end time
    if data.start_time is None or data.end_time is None:
        print("ERROR: Start and end time for partial cover unset!")
        return False

    padding_title = first.title
    center_title = "Open Shift (Cover for %s)" % data.actor if data.post else "%s (Cover for %s)" % (data.actor, first.owner)
    # See comment on end repeat in full_cover for explanation
    end_repeat = get_end_repeat(shifts.last().shift_date, data.permanent)

    # Build three events now and cut the ones we won't need
    events = [
        build_event(
            title=padding_title,
            start=og_start,
            end=data.start_time,
            end_repeat=end_repeat,
            sob_story="" if data.post else sob_story,
        ),
        build_event(
            title=center_title,
            start=data.start_time,
            end=data.end_time,
            end_repeat=end_repeat,
            sob_story=data.sob_story if data.post else "",
        ),
        build_event(
            title=padding_title,
            start=data.end_time,
            end=og_end,
            end_repeat=end_repeat,
            sob_story="" if data.post else sob_story,
        )
    ]
    # Now we validate and remove any zero-length shifts
    i = 0
    while i < len(events):
        event = events[i]
        duration = get_duration(event)
        print(duration)

        if duration == 0:
            events.remove(event)
            continue
        elif duration == 15:
            print("ERROR: Events MUST be at least 30 min long!")
            return False
        i += 1

    # Now we should have a pruned and validated list of times
    # Let's send them to Google!
    new_events=[]
    for event in events:
        new_events.append(data.g_service.events().insert(calendarId=cal_id, body=event))

    print(new_events)

    return shift_email(data)


# Return the duration of an event in minutes!
def get_duration(event):
    # In order to do this, we'll have to create two datetime objects and get the timedelta
    start = datetime.datetime.strptime(event.start, '%Y-%m-%dT%H:%M:%S')
    end = datetime.datetime.strptime(event.end, '%Y-%m-%dT%H:%M:%S')
    dur = end - start
    return int(dur.seconds/60)


# Google's format for specifying end repeat: yyyymmddThhmmssZ
# Lowercase letters represent year, month, day, etc
# Uppercase letters mean actual letters in the string
# Note: timezone is UTC
def get_end_repeat(date, permanent:bool):
    return str(date).replace("-", "") + "T090000Z" if permanent else None


# Consolidate consecutive identical shifts into bigger blobs
def consolidator(data: CoverInstructions):
    # TODO: Program this!
    return cleanup(data)


def cleanup(data: CoverInstructions):
    # TODO: Program this!
    return shift_email(data)


def shift_email(data: CoverInstructions):
    return True if data else False


# Post a single full shift
def post_single_full(data: CoverInstructions):
    # First, get all our required information
    shift = Shifts.objects.get(id=data.shift_id)
    owner = shift.owner

    # Check for errors
    if shift.is_open or not owner:  # You can't post an open shift!
        print("ERROR: This shift is already open, it cannot be posted again :/")
        return False

    # Call Event Switch
    data.update_params['post'] = True
    event_switch("update", data)

    # TODO: Program Consolidator

    return True


# Take a single full shift
# Data dictionary *must* at least have the 'shift_id' and 'taker' keys defined
'''
def take_single_full(data):
    shift_id = data['shift_id']
    taker = data['taker']

    # First, get all our required information
    cover = ShiftCovers.objects.get(shift=shift_id)
    g_id = cover.shift.google_id

    # Now we gotta send the changes to Google
    cal_id = CALENDAR_LOCATION_IDS[cover.shift.location]
    service = google_api.build_service()

    # Update our models (do it before calling the Google Cal because it auto-constructs the event title for us!)
    cover.take(taker)

    # Get shift from Google
    g_shift = get_shift(service, cal_id, g_id).execute()

    g_shift['summary'] = cover.shift.title

    # Update the shift and send it back
    updated = service.events().update(
        calendarId=cal_id,
        eventId=g_id,
        body=g_shift
    ).execute()

    # TODO: Verify the event has been updated successfully (learn what updated var looks like on failure)
    print(updated)

    cover.save()
    return True
'''


def post_permanent_full(data):

    return True


def take_permanent_full(data):

    return True


def post_single_partial(data):

    return True


def take_single_partial(data):

    return True


def post_permanent_partial(data):

    return True


def take_permanent_partial(data):

    return True

######################################################
# Helper functions


# Get an event from Google based on calendar ID and event ID
def get_shift(service, cal_id, event_id):
    return service.events().get(
        calendarId=cal_id,
        eventId=event_id
    ).execute()


# Expects start and end to be properly formatted datetime strings with timezone
# Use the startdatetime and enddatetime methods
def build_event(title, start: datetime, end: datetime, end_repeat="", sob_story=""):
    print(end_repeat)
    recurrence = "RRULE:FREQ=WEEKLY;UNTIL=%s" % end_repeat if end_repeat and end_repeat != "" else None
    # TODO: Research if people want to be added as attendees to the events

    return {
        'summary': title,
        'description': sob_story,
        'start': {
            'dateTime': start.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2]+":00",  # This is a bit sketchy but it works!
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2]+":00",
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [recurrence],
    }


def event_switch(e_type, data: CoverInstructions):
    switch = {
        'create': event_create,
        'update': event_update,
        'delete': event_delete,
    }
    return switch[e_type](data)


def event_create(data: CoverInstructions):
    # First create the event in the db, then select it for update!
    return True

'''
def event_update(data: CoverInstructions):
    # Create a write lock on the table while modification is taking place
    shift = Shifts.objects.select_for_update().filter(id=data.shift_id)

    # In general, we first update the models, then update Google, then save the updated model to the database
    # Model updates take place here in this block of 'if's (it also checks for errors)
    if data.update_params['post'] is None:
        print("No update parameters specified to event update! Can't post the cover :(")
        # Release write lock
        shift.save()
        return False

    # If this is a posted shift cover
    elif data.update_params['post']:
        # If posting, create a ShiftCover object
        new_title = "Open Shift (Cover for %s)" % (str(shift.owner))

        # Build the shift cover model
        cover = ShiftCovers(
            shift=shift,
            poster=shift.owner,
            taker=None,
            sob_story=data.sob_story,
        )
        shift.is_open = True
        shift.title = new_title

    # If this is a taken shift cover
    else:
        cover = ShiftCovers.objects.get(shift=shift)
        new_title = cover.take(data.actor)

    # Second, push changes to Google (works the same way regardless of post or take)
    cal_id = CALENDAR_LOCATION_IDS[shift.location]
    g_shift = get_shift(data.g_service, cal_id, shift.google_id)

    g_shift['summary'] = new_title

    # Update the shift and send it back
    updated = data.g_service.events().update(
        calendarId=cal_id,
        eventId=shift.google_id,
        body=g_shift
    ).execute()

    print(updated)

    # Finally, save model changes to database
    cover.save()
    shift.save()
    return True
'''


def event_delete(data: CoverInstructions):
    shifts = Shifts.objects.select_for_update().filter(Q(id=data.shift_id) | Q(permanent=data.shift_id))

    cal_id = CALENDAR_LOCATION_IDS[shifts.get(0).location]
    delete = data.g_service.events().delete(calenderId=cal_id, eventId=data.shift_id).execute()
    print(delete)  # so we can figure out what this looks like

    # On success, delete all instances from our database
    shifts.delete()
    return True
