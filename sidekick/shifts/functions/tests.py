from shifts.functions.cover import CoverInstructions
from shifts.views import push_cover
from homebase.models import Employees

# This file can be used to test the functionality of the shift covers function!
# It should be modified when new features are added to test them out.


class Test:
    test_count = 0

    def __init__(self,
                 test_input: dict,
                 expected_output: dict,
                 test_function,
                 validation_function,
                 name: str="test_"+str(test_count),
                 ):
        self.name = name
        self.test_function = test_function
        self.test_input = test_input
        self.expected_output = expected_output
        self.validation_function = validation_function

    def run(self):
        result = self.test_function(self.test_input)
        return self.validation_function(self.test_input, self.expected_output, result)


class TestArray:
    hi = "hi"


# This function tests all possible outcomes
def test_all():
    test = CoverInstructions(
        post=True,
        permanent=True,
        partial=False,
        shift_id=1,
        actor=Employees.objects.get(netid='nchera13'),
        sob_story="This is only a test"
    )
    # TODO: Finish this up
