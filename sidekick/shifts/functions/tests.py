from shifts.functions import cover
from homebase.models import Employees

# This file can be used to test the functionality of the shift covers function!
# It should be modified when new features are added to test them out.


# This function tests all possible outcomes
def test_all():
    test = cover.CoverInstructions(
        post=True,
        permanent=True,
        partial=False,
        shift_id=1,
        actor=Employees.objects.get(netid='nchera13'),
        sob_story="This is only a test"
    )
    # TODO: Finish this up
