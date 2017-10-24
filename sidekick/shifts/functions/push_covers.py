from shifts.models import Shifts, ShiftCovers, PermanentShifts
from homebase.models import Employees


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
    print(shift_id)

    # Get all our required information
    shift = Shifts.objects.get(id=shift_id)[0]
    owner = shift.owner
    if shift.is_open or not owner:  # Can't post an open shift!
        print("ERROR: This shift is already open, it cannot be posted again :/")
        return None

    # Next up, we build the shift cover
    cover = ShiftCovers(
        shift=shift,
        poster=owner,
        taker=None,
        type='sf',
        sob_story=sob_story
    )
    shift.is_open = True
    shift.title = "Open Shift (Cover for %s)" % (str(shift.owner))

    # Now we gotta send the changes to Google
    cal_id = get_location_id[shift.location]
    # TODO: construct service and get event, switch summary, then push again

    # Finally, save database changes
    cover.save()
    shift.save()


    return True

def take_single_ful(shift_id, taker:Employees):
    return True

######################################################
# Helper functions
