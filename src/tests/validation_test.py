import unittest

from services import validation

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.operators = [ord('+'),ord('-'),ord('*'),ord('/'),ord('^')]
        self.functions = [[ord('s'),ord('i'),ord('n')],[ord('c'),ord('o'),ord('s')],[ord('t'),ord('a'),ord('n')],[ord('m'),ord('a'),ord('x')],[ord('m'),ord('i'),ord('n')],[ord('l'),ord('n')],[ord('l'),ord('o'),ord('g')],[ord('s'),ord('q'),ord('r'),ord('t')],[ord('p'),ord('i')],[ord('e')]]
        self.ranges = {'A_to_Z': range(ord('A'),ord('Z')+1),
                  'a_to_z': range(ord('a'),ord('z')+1),
                  '0_to_9': range(ord('0'),ord('9')+1)}
        self.ints = {'(': ord('('),
                ')': ord(')'),
                ',': ord(','),
                '.': ord('.')}

        self.validator = validation.Validator(self.operators, self.functions, self.ranges, self.ints)

    def test_validation_ranges_and_ints_are_set_correctly(self):
        self.assertEqual([self.validator._ops, self.validator._fns, self.validator._ranges, self.validator._ints], [self.operators, self.functions, self.ranges, self.ints])

    def test_get_calling_function_name_returns_calling_function_name(self):
        self.assertEqual(self.validator.get_calling_function_name(), "Test get calling function name returns calling function name!")

    def test_unassigned_variables_used_returns_empty_string_when_only_assigned_variables(self):
        self.assertEqual(self.validator.unassigned_variables_used([[ord("A")],[ord("B")]], {"A": 1, "B": 2}),"")

    def test_unassigned_variables_used_returns_its_name_when_unassigned_variables(self):
        self.assertEqual(self.validator.unassigned_variables_used([[ord("A")],[ord("C")]], {"A": 1, "B": 2}),"Unassigned variables used!")

    def test_invalid_use_of_operators_returns_its_name_with_operator_at_beginning(self):
        self.assertEqual(self.validator.invalid_use_of_operators([[ord("+")],[ord("1")],[ord("+")],[ord("2")]]), "Invalid use of operators!")

    def test_invalid_use_of_operators_returns_its_name_with_operator_at_end(self):
        self.assertEqual(self.validator.invalid_use_of_operators([[ord("1")],[ord("+")],[ord("2")],[ord("+")]]), "Invalid use of operators!")

    def test_invalid_use_of_operators_returns_its_name_with_two_operators_in_middle(self):
        self.assertEqual(self.validator.invalid_use_of_operators([[ord("1")],[ord("+")],[ord("+")],[ord("2")]]), "Invalid use of operators!")

    def test_invalid_use_of_dot_returns_its_name(self):
        self.assertEqual(self.validator.invalid_use_of_dot([[ord("1")],[ord("+")],[ord("2")],[ord(".")]]), "Invalid use of dot!")

    def test_missing_operator_returns_empty_string_when_no_operator_is_missing(self):
        start_and_end_in_parentheses = [[ord('(')],[ord('1')],[ord('+')],[ord('2')],[ord(')')]]
        start_with_number =[[ord('3')],[ord('*')],[ord('(')],[ord('1')],[ord('+')],[ord('2')],[ord(')')]]
        end_with_number = [[ord('(')],[ord('1')],[ord('+')],[ord('2')],[ord(')')],[ord('*')],[ord('3')]]
        inputs = [start_and_end_in_parentheses, start_with_number, end_with_number]

        outputs = []
        for input in inputs:
            outputs.append(self.validator.missing_operator(input))

        self.assertEqual(outputs, [""]*len(outputs))

    def test_missing_operator_returns_its_name_when_operator_is_missing(self):
        op_missing_before_left_parenthesis = [[ord('3')],[ord('(')],[ord('1')],[ord('+')],[ord('2')],[ord(')')]]
        op_missing_after_right_parenthesis = [[ord('(')],[ord('1')],[ord('+')],[ord('2')],[ord(')')],[ord('3')]]
        inputs = [op_missing_before_left_parenthesis, op_missing_after_right_parenthesis]

        outputs = []
        for input in inputs:
            outputs.append(self.validator.missing_operator(input))

        self.assertEqual(outputs, ["Missing operator!"]*len(outputs))
