from django.db.models import Q, ObjectDoesNotExist
from django.core.mail import send_mail, send_mass_mail
from shifts.models import Shifts, Holidays
from homebase.models import Employees
from shifts.functions import google_api
from sidekick.settings import CALENDAR_LOCATION_IDS
import datetime
import copy
import pytz


# Class that details instructions for posting and taking shift covers
# Note: because this initializes a google service, it should only be created when we *know* a cover will take place
class CoverInstructions:
    def __init__(self, post, permanent, partial, shift_id, actor: Employees, start_time=None,
                 end_time=None, sob_story=""):
        self.post = post
        self.permanent = permanent
        self.partial = partial
        self.shift_id = shift_id
        self.actor = actor
        self.start_time = start_time
        self.end_time = end_time
        self.sob_story = sob_story
        self.g_service = google_api.build_service()  # build at create time

    def push(self):
        return push_cover_new(self)


def push_cover_new(data: CoverInstructions):
    # Validation
        # On error: notify user
    data, outcome = validate_cover(data)

    print(outcome)
    if outcome != "valid":
        return {"result": "failed", "description": outcome}

    # Get shift instance
    shift = Shifts.objects.filter(event_id=data.shift_id).first()

    # Transform start and end times to be timezone-aware
    tz = pytz.timezone("America/Los_Angeles")
    start = tz.localize(shift.shift_start)
    end = tz.localize(shift.shift_end)

    # Figure out the name of the old owner (tf the shift had no owner before, this is blank)
    if shift.owner_id:
        old_owner_name = Employees.objects.get(netid=shift.owner_id).full_name
    else:
        old_owner_name = None
    actor_name = data.actor.full_name

    # Build event recurrence for permanent shifts!
    if data.permanent:
        # We'll build the standard recurrence here and edit it later
        print("OG Recurrence")
        perm_id = data.shift_id.split("_")[0]
        last_shift = Shifts.objects.filter(permanent_id=perm_id).order_by('shift_date').last()
        recurrence = build_recurrence(last_shift.shift_date, perm_id)
    else:
        recurrence = None

    if data.post:
        sob_story = data.sob_story
    else:
        sob_story = shift.sob_story

    # If partial, assemble the partial events
    events = []
    if data.partial:
        if data.post:
            partial_title = actor_name
        else:
            if old_owner_name:
                partial_title = "Open Shift (Cover for %s)" % old_owner_name
            else:
                partial_title = "Open Shift"

        if start < data.start_time:
            print("Start padding recurrence")
            st_recurrence = edit_recurrence(recurrence, start)
            events.append(build_event(
                title=partial_title,
                start=start,
                end=data.start_time,
                recurrence=st_recurrence,
                sob_story="" if data.post else sob_story,
            ))

        if data.end_time < end:
            print("End padding recurrence")
            en_recurrence = edit_recurrence(recurrence, data.end_time)
            events.append(build_event(
                title=partial_title,
                start=data.end_time,
                end=end,
                recurrence=en_recurrence,
                sob_story="" if data.post else sob_story,
            ))

    # Build main event
    if data.post:
        main_title = "Open Shift (Cover for %s)" % old_owner_name
    elif old_owner_name:
        main_title = "%s (Cover for %s)" % (actor_name, old_owner_name)
    else:
        main_title = actor_name

    if data.partial:
        recurrence = edit_recurrence(recurrence, data.start_time)

    events.append(build_event(
        title=main_title,
        start=data.start_time,
        end=data.end_time,
        recurrence=recurrence,
        sob_story="" if not data.post else sob_story,
    ))

    # Send cover to Google
    cal_id = CALENDAR_LOCATION_IDS[shift.location]
    new_events = []
    for event in events:
        new_events.append(data.g_service.events().insert(calendarId=cal_id, body=event).execute())

    # Delete old event from Google
    if data.permanent:
        old_id = data.shift_id.split("_")[0]
    else:
        old_id = data.shift_id

    data.g_service.events().delete(
        calendarId=cal_id,
        eventId=old_id
    ).execute()

    return {"result": "success", "description": "Your cover was successfully pushed!"}


def validate_cover(data: CoverInstructions):
    outcome = "valid"
    # Ensure booleans for type indicators
    data.post = bool(data.post)
    data.permanent = bool(data.permanent)
    data.partial = bool(data.partial)

    data.shift_id = str(data.shift_id)

    # Validate actor
    if not isinstance(data.actor, Employees):
        outcome = "Bad actor data!"
        return data, outcome

    # Validate shift (ensure the shift id is valid)
    shifts = Shifts.objects.filter(event_id=data.shift_id)
    if len(shifts) == 0 or len(shifts) > 1:
        outcome = "Bad shift ID specified"
        return data, outcome

    tz = pytz.timezone("America/Los_Angeles")
    if data.start_time or data.end_time and data.partial:
        if not isinstance(data.start_time, datetime.datetime) or not isinstance(data.end_time, datetime.datetime):
            try:
                data.start_time = pytz.utc.localize(datetime.datetime.strptime(data.start_time+"UTC", "%Y-%m-%dT%H:%M:%S.000Z%Z"))
                data.end_time = pytz.utc.localize(datetime.datetime.strptime(data.end_time+"UTC", "%Y-%m-%dT%H:%M:%S.000Z%Z"))
                data.start_time = data.start_time.astimezone(pytz.timezone('America/Los_Angeles'))
                data.end_time = data.end_time.astimezone(pytz.timezone('America/Los_Angeles'))
            except ValueError:
                outcome = "Invalid partial start and end times"
                return data, outcome

    # Validate start and end times for partial cover or set start/end times for full cover
    shift = shifts.first()
    start = tz.localize(shift.shift_start)
    end = tz.localize(shift.shift_end)

    if data.partial and data.start_time and data.end_time:
        if start > data.start_time or end < data.end_time:
            outcome = "Start and end times are not in acceptable range!"
            return data, outcome

        if data.start_time >= data.end_time:
            outcome = "The start time must be *before* the end time!"
            return data, outcome

        # Enforce no 15 minute shift rule
        fifteen = datetime.timedelta(minutes=15)
        if data.start_time-start == fifteen or end-data.end_time == fifteen or data.end_time-data.start_time == fifteen:
            outcome = "Fifteen minute shifts are not allowed!"
            return data, outcome
    elif data.partial:
        outcome = "Partial start and end times unset."
        return data, outcome
    else:
        data.start_time = start
        data.end_time = end

    return data, outcome


# Return the duration of an event in minutes!
def get_duration(event):
    print(event)
    # In order to do this, we'll have to create two datetime objects and get the timedelta
    start = datetime.datetime.strptime(event['start']['dateTime'][:-3]+"00", '%Y-%m-%dT%H:%M:%S%z')
    end = datetime.datetime.strptime(event['end']['dateTime'][:-3]+"00", '%Y-%m-%dT%H:%M:%S%z')
    dur = end - start
    return int(dur.seconds/60)


# Consolidate consecutive identical shifts into bigger blobs
def consolidator(data: CoverInstructions):
    # TODO: Program this!
    matching_shifts = Shifts.objects.filter()
    return cleanup(data)


def cleanup(data: CoverInstructions):
    # TODO: Program this!
    return shift_notify(data)


def shift_notify(data: CoverInstructions, shift: Shifts):

    perm_str = "permanent " if data.permanent else ""
    if data.post:
        subject = "A new " + perm_str + "shift cover has been posted!"
        body = "There has been a new " + perm_str + "cover posted for " + str(shift.owner) + ".\n" + \
               "Location: " + shift.pretty_location + "\n" + \
               "Date: " + str(shift.shift_date) + "\n" + \
               "Start time: " + str(shift.shift_start) + "\n" + \
               "End time: " + str(shift.shift_end) + "\n" + \
               "Reason: " + str(shift.sob_story)

    else:
        if data.partial:
            if data.permanent:
                print('take partial permanent')
            else:
                print('take partial single')
        else:
            if data.permanent:
                print('take full permanent')
            else:
                print('take full single')

    # Full single post
        # Notify mods who share a shift (unless post is for mod calendar)
        # Notify techs for whom cover is relevant
        # Notify staff(?) (check w/ Rosa)

    # Full single take
        # Notify mods who share a shift (unless post is for mod calendar)
        # Notify tech who took
        # Notify tech who posted

    # Full permanent post
        # Notify mods sharing a shift
        # Notify relevant techs
        # Notify staff(?)

    # Full Permanent take
        # Notify mods who share shift
        # Notify relevant techs
        # Notify staff(?)

    # Partial single post
        # Notify mods who share shift w/ partial
        # Notify relevant techs
        # Notify staff(?)

    # Partial single take
        # Notify mods who share shift w/ partial
        # Notify taker
        # Notify poster (w/ reminder that they're still responsible for remaining shift)

    # Partial permanent post
        # Notify mods who share shift
        # Notify relevant techs

    # Partial permanent take
        # Notify mods
        # Notify taker
        # Notify poster (w/ reminder)
    return True


######################################################
# Helper functions


# Get an event from Google based on calendar ID and event ID
def get_shift(service, cal_id, event_id):
    return service.events().get(
        calendarId=cal_id,
        eventId=event_id
    ).execute()


# fexc = f(ormat) exc(eption): fmt exception date object as an EXDATE string
def fexc(exception: datetime.datetime):
    return "EXDATE;VALUE=DATE:%s" % exception.strftime("%Y%m%d")


# Expects start and end to be properly formatted datetime strings with timezone
# Use the startdatetime and enddatetime methods
def build_event(title: str, start: datetime, end: datetime, recurrence=None,
                sob_story=None):
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
        'recurrence': recurrence,
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
    print(recurrence)
    return recurrence


# Edit an existing instance of recurring data to a new start/end time
# Useful for partial permanent shift covers
def edit_recurrence(recurrence: list, start_time: datetime.datetime):
    if not recurrence:
        return None

    shift_time = start_time.strftime("T%H%M%S")

    try:
        exdates = str(recurrence[1])
    except IndexError:
        return recurrence

    print(exdates)
    # First, get the individual dates
    dates = exdates.split(":")[1].split(",")

    # Then paste the new times instead of the old ones
    date_string = ""
    for date in dates:
        first_half = date.split("T")[0]
        date_string += first_half + shift_time + ","

    recurrence[1] = exdates.split(":")[0] + ":" + date_string[:-1]
    print(recurrence)
    return copy.deepcopy(recurrence)


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
