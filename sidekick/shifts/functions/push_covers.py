from shifts.models import Shifts, ShiftCovers, PermanentShifts
from homebase.models import Employees
from shifts.functions import google_api
from sidekick.settings import CALENDAR_LOCATION_IDS

######################################################
# Main post/take fns

"""
'data' dictionary reserved keys:
'shift_id': the sidekick shift ID (not the google ID!)
    - Required for all cover functions

'sob_story': the reason for the cover in question
    - Required for all posting functions

'taker': the taker of a shift cover
    - Required for all taking functions
    
'start_time' and 'end_time': start and end time for partial shift covers
    - Required for all partial covers

"""



# Master routing fn (call this to route shift covers properly!)
def push_cover(shift_id, type, data):
    # This code takes advantage of the fact that you can use functions as variables in Python
    # In essence, we use the dictionary type_fns to get the right function, then call it in the return statement.
    # All the parameters for the functions will be the same, no matter what we're calling
    # We use the 'data' param as a dictionary for holding the parameters necessary for each function
    type_fns = {
        'post_single_full': post_single_full,
        'take_single_full': take_single_full,
        'post_permanent_full': post_permanent_full,
        'take_permanent_full': take_permanent_full,
        'post_single_partial': post_single_partial,
        'take_single_partial': take_single_partial,
        'post_permanent_partial': post_permanent_partial,
        'take_permanent_partial': take_permanent_partial
    }
    return type_fns[type](data)

# Post a single full shift
# Data dictionary *must* at least have the 'shift_id' and 'sob_story' keys defined
def post_single_full(data):
    shift_id = data['shift_id']

    # First, get all our required information
    shift_get = Shifts.objects.get(id=shift_id)[0]
    shift = [s for s in shift_get][0]
    owner = shift.owner

    # Check for errors
    if shift.is_open or not owner:  # You can't post an open shift!
        print("ERROR: This shift is already open, it cannot be posted again :/")
        return False


    new_title = "Open Shift (Cover for %s)" % (str(owner))

    # Next up, we build the shift cover model
    cover = ShiftCovers(
        shift=shift,
        poster=owner,
        taker=None,
        type='sf',
        sob_story=data['sob_story'],
        permanent=False
    )
    shift.is_open = True
    shift.title = new_title

    # Now we gotta send the changes to Google
    cal_id = CALENDAR_LOCATION_IDS[shift.location]
    service = google_api.build_service()

    # Get shift from Google
    g_shift = get_shift(service,cal_id, shift.google_id).execute()

    print(shift)

    g_shift['summary'] = new_title

    # Update the shift and send it back
    updated = service.events().update(
        calendarId=cal_id,
        eventId=shift.google_id,
        body=g_shift
    ).execute()

    # TODO: Verify the event has been updated successfully (learn what updated var looks like on failure)
    print(updated)

    # Finally, save database changes
    cover.save()
    shift.save()

    return updated

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
def build_shift(title, start, end, recurrent:bool, sob_story = ""):
    recurrence = "RRULE:FREQ=WEEKLY;UNTIL:20171216070000Z" if recurrent else None
    #TODO: Research if people want to be added as attendees to the events

    return {
        'summary': title,
        'description': sob_story,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America,Los_Angeles'
        },
        'recurrence': [recurrence],
    }
