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
    # TODO: Get more in here
}

######################################################
# Main post/take fns


# Post a single full shift
def post_single_full(shift_id, sob_story):
    global get_location_id
    print(shift_id)

    # First, get all our required information
    shift = Shifts.objects.get(id=shift_id)[0]
    owner = shift.owner
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
        sob_story=sob_story
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

def take_single_full(shift_id, taker:Employees):
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
