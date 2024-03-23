import unittest

from services import validation

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_incorrect_brackets_returns_false_when_brackets_ok(self):
        input = [ord("("), ord(")")]
        result = validation.incorrect_brackets(input)
        self.assertEqual(result, False)

    def test_incorrect_brackets_founds_brackets_that_are_wrong_way_around(self):
        input = [ord(")"), ord("(")]
        result = validation.incorrect_brackets(input)
        self.assertEqual(result, True)

    def test_unassigned_variables_returns_false_when_only_assigned_variables(self):
        self.assertEqual(validation.unassigned_variables([ord("B"),ord("C")], range(ord("A"),ord("Z")+1), range(ord("B"),ord("D")+1)), False)

    def test_unassigned_variables_returns_true_when_unassigned_variables(self):
        self.assertEqual(validation.unassigned_variables([ord("E")], range(ord("A"),ord("Z")+1), range(ord("B"),ord("D")+1)), True)
