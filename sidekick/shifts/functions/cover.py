from django.db.models import Q
<<<<<<< HEAD
from shifts.models import Shifts, ShiftCovers
=======
from django.core.mail import send_mail, send_mass_mail
from shifts.models import Shifts, Holidays
>>>>>>> develop
from homebase.models import Employees
from shifts.functions import google_api
from sidekick.settings import CALENDAR_LOCATION_IDS
import datetime
import pytz


# Class that details instructions for posting and taking shift covers
<<<<<<< HEAD
# Note: because this initializes a google service, it should only be created we *know* a cover will take place
class CoverInstructions:
    def __init__(self, post, permanent, partial, shift_id, actor: Employees, start_time: datetime.datetime=None,
                 end_time: datetime.datetime=None, sob_story=""):
=======
# Note: because this initializes a google service, it should only be created when we *know* a cover will take place
class CoverInstructions:
    def __init__(self, post, permanent, partial, shift_id, actor: Employees, start_time=None,
                 end_time=None, sob_story=""):
>>>>>>> develop
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

<<<<<<< HEAD

######################################################
# Main post/take fns
# Master routing fn (call this to route shift covers properly!)
def push_cover(data: CoverInstructions):
=======
    def push(self):
        return push_cover(self)


##############################################################
# Main post/take fns
# Master routing fn (called by CoverInstructions, routes shift covers properly!)
def push_cover(data: CoverInstructions):
    # TODO: Verification before covers!
>>>>>>> develop
    return partial_cover(data) if data.partial else full_cover(data)


# For full covers of any kind
def full_cover(data: CoverInstructions):
    print('FullCover called!')
<<<<<<< HEAD
=======

>>>>>>> develop
    # 1. Get all shifts associated with this cover (could be one or many)
    shifts = Shifts.objects.filter(event_id__contains=data.shift_id).order_by('shift_date')
    print([s for s in shifts])

    # 2. Save some useful attributes for later
    first = shifts.first()
    # Verify shift exists in our db
    if first is None:
        print("Shift does not exist!")
<<<<<<< HEAD
        return False
=======
        return "Failed: Shift does not exist in db"
>>>>>>> develop

    location = first.location
    cal_id = CALENDAR_LOCATION_IDS[location]
    tz = pytz.timezone('America/Los_Angeles')

<<<<<<< HEAD
    old_event_id = first.permanent_id
    print(old_event_id)

    # Define the shift owner
    owner = first.owner if data.post else data.actor

    # Construct new title
    if data.post:
        new_title = "Open Shift (Cover for %s)" % data.actor
=======
    old_event_id = first.permanent_id if data.permanent else first.event_id
    print(old_event_id)

    # Define the shift owner
    owner = data.actor if data.post else first.owner

    # Construct new title
    if data.post:
        new_title = "Open Shift (Cover for %s)" % owner
>>>>>>> develop
    else:
        new_title = "%s (Cover for %s)" % (data.actor, owner)

    # 3. Create new Google Event
    # Start by figuring out the end repeat date if necessary
<<<<<<< HEAD
    end_repeat = get_end_repeat(shifts.last().shift_date, data.permanent)
=======
    end_repeat = shifts.last().shift_date
>>>>>>> develop

    # Construct event
    event = build_event(
        title=new_title,
        start=tz.localize(first.shift_start),
        end=tz.localize(first.shift_end),
        end_repeat=end_repeat,
<<<<<<< HEAD
        sob_story=data.sob_story
=======
        sob_story=data.sob_story,
        old_permanent_id=first.permanent_id if data.permanent else None,
>>>>>>> develop
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

<<<<<<< HEAD
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

    return consolidator(data)
=======
    return shift_email(data)
>>>>>>> develop


# For partial covers of any kind
# Unfortunately, this is a good deal more complex than full covers :/
def partial_cover(data: CoverInstructions):
<<<<<<< HEAD
=======
    tz = pytz.timezone('America/Los_Angeles')
>>>>>>> develop
    # 1. Get all shifts associated with cover (could be 1 or many)
    shifts = Shifts.objects.filter(event_id__contains=data.shift_id).order_by('shift_date')

    # 2. Save some useful attributes for later
    first = shifts.first()
    # Verify shift exists in our db
    if first is None:
        print("Shift does not exist!")
<<<<<<< HEAD
        return False
=======
        return "Failed: Shift does not exist in db"
>>>>>>> develop

    location = first.location
    cal_id = CALENDAR_LOCATION_IDS[location]
    old_event_id = first.permanent_id
<<<<<<< HEAD
    og_start = datetime.datetime(first.shift_start)
    og_end = datetime.datetime(first.shift_end)
    if not data.post:
        cover = ShiftCovers.objects.get(shift__contains=data.shift_id)
        sob_story = cover.sob_story
=======
    og_start = tz.localize(first.shift_start)
    og_end = tz.localize(first.shift_end)
    print(data.start_time)
    print(data.end_time)
    new_start = pytz.utc.localize(datetime.datetime.strptime(data.start_time, "%Y-%m-%dT%H:%M:%S.000Z"))
    new_end = pytz.utc.localize(datetime.datetime.strptime(data.end_time, "%Y-%m-%dT%H:%M:%S.000Z"))
    print(new_start)
    print(new_end)
    if not data.post:
        sob_story = first.sob_story
>>>>>>> develop
    else:
        sob_story = ""

    # 3. Figure out how to split shift using start and end times
    # Start by doing basic validation on start & end time
    if data.start_time is None or data.end_time is None:
        print("ERROR: Start and end time for partial cover unset!")
<<<<<<< HEAD
        return False
=======
        return "Failed: Start and end time for partial cover are unset!"
>>>>>>> develop

    padding_title = first.title
    center_title = "Open Shift (Cover for %s)" % data.actor if data.post else "%s (Cover for %s)" % (data.actor, first.owner)
    # See comment on end repeat in full_cover for explanation
<<<<<<< HEAD
    end_repeat = get_end_repeat(shifts.last().shift_date, data.permanent)
=======
    end_repeat = shifts.last().shift_date
>>>>>>> develop

    # Build three events now and cut the ones we won't need
    events = [
        build_event(
            title=padding_title,
            start=og_start,
<<<<<<< HEAD
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
    # Now we validate and remove any zero-length shift
    i=0
    while i < len(events):
        event = events[i]
        duration = get_duration(event)
=======
            end=new_start,
            end_repeat=end_repeat,
            sob_story="" if data.post else sob_story,
            old_permanent_id=first.permanent_id if data.permanent else None,
        ),
        build_event(
            title=center_title,
            start=new_start,
            end=new_end,
            end_repeat=end_repeat,
            sob_story=data.sob_story if data.post else "",
            old_permanent_id=first.permanent_id if data.permanent else None,
        ),
        build_event(
            title=padding_title,
            start=new_end,
            end=og_end,
            end_repeat=end_repeat,
            sob_story="" if data.post else sob_story,
            old_permanent_id=first.permanent_id if data.permanent else None,
        )
    ]
    # Now we validate and remove any zero-length shifts
    i = 0
    while i < len(events):
        event = events[i]
        duration = get_duration(event)
        print(duration)
>>>>>>> develop

        if duration == 0:
            events.remove(event)
            continue
        elif duration == 15:
            print("ERROR: Events MUST be at least 30 min long!")
<<<<<<< HEAD
            return False
        i += 1

    # Now we should have a pruned and validated list of times


    return consolidator(data)
=======
            return "Failed: All shifts must be at least 30 min long!"
        i += 1

    # Now we should have a pruned and validated list of times
    # Let's send them to Google!
    new_events=[]
    for event in events:
        new_events.append(data.g_service.events().insert(calendarId=cal_id, body=event).execute())

    print(new_events)

    return shift_email(data)
>>>>>>> develop


# Return the duration of an event in minutes!
def get_duration(event):
<<<<<<< HEAD
    return 5


# Google's format for specifying end repeat: yyyymmddThhmmssZ
# Lowercase letters represent year, month, day, etc
# Uppercase letters mean actual letters in the string
# Note: timezone is UTC
def get_end_repeat(date, permanent:bool):
    return str(date).replace("-", "") + "T090000Z" if permanent else None
=======
    print(event)
    # In order to do this, we'll have to create two datetime objects and get the timedelta
    start = datetime.datetime.strptime(event['start']['dateTime'][:-3]+"00", '%Y-%m-%dT%H:%M:%S%z')
    end = datetime.datetime.strptime(event['end']['dateTime'][:-3]+"00", '%Y-%m-%dT%H:%M:%S%z')
    dur = end - start
    return int(dur.seconds/60)
>>>>>>> develop


# Consolidate consecutive identical shifts into bigger blobs
def consolidator(data: CoverInstructions):
    # TODO: Program this!
<<<<<<< HEAD
=======
    matching_shifts = Shifts.objects.filter()
>>>>>>> develop
    return cleanup(data)


def cleanup(data: CoverInstructions):
    # TODO: Program this!
    return shift_email(data)


def shift_email(data: CoverInstructions):
<<<<<<< HEAD
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


def post_permanent_full(data):

    return True


def take_permanent_full(data):

    return True


def post_single_partial(data):

    return True


def take_single_partial(data):

    return True


def post_permanent_partial(data):
=======
    # TODO: Program this
    return True


def mail_test():
    send_mail(
        subject="This is a test!",
        message="Hi you!",
        from_email="testy@sidekick.apu.edu",
        recipient_list=["nchera13@apu.edu"],
        fail_silently=False,
    )
>>>>>>> develop

    return True


<<<<<<< HEAD
def take_permanent_partial(data):

    return True

=======
>>>>>>> develop
######################################################
# Helper functions


# Get an event from Google based on calendar ID and event ID
def get_shift(service, cal_id, event_id):
    return service.events().get(
        calendarId=cal_id,
        eventId=event_id
    ).execute()


<<<<<<< HEAD
# Expects start and end to be properly formatted datetime strings with timezone
# Use the startdatetime and enddatetime methods
def build_event(title, start: datetime, end: datetime, end_repeat="", sob_story=""):
    print(end_repeat)
    recurrence = "RRULE:FREQ=WEEKLY;UNTIL=%s" % end_repeat if end_repeat and end_repeat != "" else None
=======
# fexc = f(ormat) exc(eption): fmt exception date object as an EXDATE string
def fexc(exception: datetime.datetime):
    return "EXDATE;VALUE=DATE:%s" % exception.strftime("%Y%m%d")


# Expects start and end to be properly formatted datetime strings with timezone
# Use the startdatetime and enddatetime methods
def build_event(title: str, start: datetime, end: datetime, end_repeat=datetime.datetime.now(),
                sob_story=None, old_permanent_id=None):
>>>>>>> develop
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
<<<<<<< HEAD
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


def event_delete(data: CoverInstructions):
    shifts = Shifts.objects.select_for_update().filter(Q(id=data.shift_id) | Q(permanent=data.shift_id))

    cal_id = CALENDAR_LOCATION_IDS[shifts.get(0).location]
    delete = data.g_service.events().delete(calenderId=cal_id, eventId=data.shift_id).execute()
    print(delete)  # so we can figure out what this looks like

    # On success, delete all instances from our database
    shifts.delete()
    return True
=======
        'recurrence': build_recurrence(end_repeat, old_permanent_id),
    }


# Build the recurrence list for the Google calendar, making sure to list exceptions
# For details, see https://developers.google.com/google-apps/calendar/concepts/events-calendars#recurring_events
def build_recurrence(end_repeat: datetime.datetime, permanent_id: str):
    # For non-permanent shifts
    if not permanent_id:
        return None

    recurrence = ["RRULE:FREQ=WEEKLY;UNTIL=%s" % get_end_repeat(end_repeat)]
    exceptions = get_exceptions(permanent_id)
    if exceptions:
        recurrence.append(exceptions)
    return recurrence


# Google's format for specifying end repeat: yyyymmddThhmmssZ
# Lowercase letters represent year, month, day, etc
# Uppercase letters mean actual letters in the string
# Note: timezone is UTC
# Note: we increment the day to make sure the last instance of the shift doesn't get cut off
def get_end_repeat(date: datetime.datetime):
    date = date + datetime.timedelta(days=1)
    return str(date).replace("-", "") + "T090000Z"


# Returns a list of EXDATE strings that will be used to exclude dates from a recurring event
# There are two reasons this could happen:
# 1. The user posted a single shift cover and then posted a permanent shift cover
# 2. The day in question is a holiday
def get_exceptions(permanent_id):
    exceptions = []

    shifts = Shifts.objects.filter(permanent_id=permanent_id).order_by('shift_start')
    shift_dates = [s.shift_date for s in shifts]

    # First, we need to get a list of holidays that the shift overlaps with
    holidays = Holidays.objects.all()
    holiday_dates = [h.date for h in holidays]

    # Check to see if any of our dates are holidays
    for s in shift_dates:
        if s in holiday_dates:
            exceptions.append(s)

    # Next, check for excluded weeks (where single shift covers may have been posted or they were deleted from the cal)
    date_increment = shifts.first().shift_start

    index = 0
    while date_increment <= shifts.last().shift_start:
        shift = shifts[index]
        if shift.shift_start != date_increment:
            exceptions.append(date_increment)
        else:
            index += 1
        date_increment += datetime.timedelta(weeks=1)

    e_str = ""
    if exceptions:
        e_str = "EXDATE;TZID=America/Los_Angeles:"
        for exception in exceptions:
            e_str += exception.strftime("%Y%m%dT%H%M%S")+","

    return e_str[:-1]
>>>>>>> develop
