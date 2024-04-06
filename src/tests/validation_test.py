import unittest

from services import validation

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = validation.Validator()

    def test_input_is_set_correctly(self):
        input_elements = [[1], [1,2,3], [11,12]]
        variables = {'A': 1, 'B': 2, 'C': 3}
        self.validator.set_input(input_elements, variables)
        self.assertEqual([self.validator._input_elements, self.validator._variables], [input_elements, variables])

    def test_unassigned_variables_returns_false_when_only_assigned_variables(self):
        self.validator.set_input([[ord("A")],[ord("B")]], {"A": 1, "B": 2})
        self.assertEqual(self.validator.unassigned_variables(), False)

    def test_unassigned_variables_returns_true_when_unassigned_variables(self):
        self.validator.set_input([[ord("A")],[ord("C")]], {"A": 1, "B": 2})
        self.assertEqual(self.validator.unassigned_variables(), True)

    def test_improper_operator_use_returns_true_with_operator_at_beginning(self):
        self.validator.set_input([[ord("+")],[ord("1")],[ord("+")],[ord("2")]], {})
        self.assertEqual(self.validator.improper_operator_use(), True)

    def test_improper_operator_use_returns_true_with_operator_at_end(self):
        self.validator.set_input([[ord("1")],[ord("+")],[ord("2")],[ord("+")]], {})
        self.assertEqual(self.validator.improper_operator_use(), True)

    def test_improper_operator_use_returns_true_with_two_operators_in_middle(self):
        self.validator.set_input([[ord("1")],[ord("+")],[ord("+")],[ord("2")]], {})
        self.assertEqual(self.validator.improper_operator_use(), True)

    def test_lone_dot_returns_true(self):
        self.validator.set_input([[ord("1")],[ord("+")],[ord("2")],[ord(".")]], {})
        self.assertEqual(self.validator.lone_dot_found(), True)
