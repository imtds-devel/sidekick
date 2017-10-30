from shifts.models import Shifts, ShiftCovers, PermanentShifts
from homebase.models import Employees
from shifts.functions import google_api


get_location_id = {
    'ma': 'apu.edu_1et1nvtkk2h104q23odp8d80qk@group.calendar.google.com',
    'da': 'apu.edu_4k6lbta718h17tao2s7env9vsg@group.calendar.google.com',
    'st': 'apu.edu_b09rl73hfmh0nmu8fplnbetlt8@group.calendar.google.com',
    'sd': 'apu.edu_ohl01622csflosjt3io4d3gfsk@group.calendar.google.com',
    'rc': 'apu.edu_9rei5vi75v3vmo2revbbi43pts@group.calendar.google.com',
    'md': 'apu.edu_qo3fjdiio82sou892a265fnkc4@group.calendar.google.com',
    'te': 'primary'
    # TODO: Get more in here
}

######################################################
# Main post/take fns

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
    global get_location_id
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
        sob_story=data['sob_story']
    )
    shift.is_open = True
    shift.title = new_title

    # Now we gotta send the changes to Google
    cal_id = get_location_id[shift.location]
    service = google_api.build_service()

    # Get shift from Google
    shift = get_shift(service,cal_id, shift.google_id)

    print(shift)

    shift['summary'] = new_title

    # Update the shift and send it back
    updated = service.events().update(
        calendarId=cal_id,
        eventId = shift.google_id
    )

    # TODO: Verify the event has been updated successfully (learn what updated var looks like on failure)

    # Finally, save database changes
    cover.save()
    shift.save()

    return updated

def take_single_full(data):
    global get_location_id


    return True

def post_permanent_full(data):
    global get_location_id


    return True

def take_permanent_full(data):
    global get_location_id


    return True

def post_single_partial(data):
    global get_location_id


    return True

def take_single_partial(data):
    global get_location_id


    return True

def post_permanent_partial(data):
    global get_location_id


    return True

def take_permanent_partial(data):
    global get_location_id


    return True

######################################################
# Helper functions

# Get an event from Google based on calendar ID and event ID
def get_shift(service, cal_id, event_id):
    return service.events().get(
        calendarId=cal_id,
        eventId=event_id
    )

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
