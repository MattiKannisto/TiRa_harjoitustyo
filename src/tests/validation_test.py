import unittest
from decimal import Decimal

from services import validation

class TestValidation(unittest.TestCase):

    def setUp(self):
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

    def test_numbers_too_large_to_be_computed_return_its_name_with_too_large_numbers(self):
        input = Decimal(4234324)**Decimal(3432523424)
        result = self.validator.numbers_too_large_to_be_computed(input)
        self.assertEqual(result, "Numbers too large to be computed!")

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

    def test_unknown_function_used_returns_its_name_with_lowercase_alphabets_not_used_in_functions(self):
        input = [[ord('p'),ord('r'),ord('i'),ord('n'),ord('t')],[ord('(')],[ord('3')],[ord('+')],[ord('4')],[ord(')')]]
        result = self.validator.unknown_function_used(input)
        self.assertEqual(result, "Unknown function used!")

    def test_invalid_use_of_dot_returns_its_name(self):
        self.assertEqual(self.validator.invalid_use_of_dot([[ord("1")],[ord("+")],[ord("2")],[ord(".")]]), "Invalid use of dot!")

    def test_invalid_use_of_functions_returns_its_name_when_using_incorrect_number_of_arguments(self):
        inputs = [[[ord('s'),ord('i'),ord('n')],[ord('(')],[ord('1')],[ord(',')],[ord('3')],[ord(')')]],
                  [[ord('m'),ord('a'),ord('x')],[ord('(')],[ord('1')],[ord(')')]]]
        results = [self.validator.invalid_use_of_functions(input) for input in inputs]
        self.assertEqual(results, ["Invalid use of functions!"]*len(results))

    def test_missing_function_argument_returns_its_name_with_missing_arguments(self):
        inputs = [[[ord('s'),ord('i'),ord('n')],[ord('(')],[ord(')')]],
                  [[ord('m'),ord('a'),ord('x')],[ord('(')],[ord('1')],[ord(',')],[ord(')')]],
                  [[ord('m'),ord('a'),ord('x')],[ord('(')],[ord(',')],[ord('1')],[ord(')')]],
                  [[ord('m'),ord('a'),ord('x')],[ord('(')],[ord(',')],[ord(')')]]]
        results = [self.validator.missing_function_argument(input) for input in inputs]
        self.assertEqual(results, ["Missing function argument!"]*len(results))  

    def test_missing_function_returns_its_name_with_missing_function_name(self):
        inputs = [[[ord('3')],[ord(',')],[ord('3')]],
                  [[ord('(')],[ord('3')],[ord(',')],[ord('3')],[ord(')')]],
                  [[ord('s'),ord('i'),ord('n')],[ord('(')],[ord('(')],[ord('3')],[ord(',')],[ord('3')],[ord(')')],[ord(')')]]]
        results = [self.validator.missing_function(input) for input in inputs]
        self.assertEqual(results, ["Missing function!"]*len(results))

    def test_missing_function_returns_empty_string_with_valid_inputs(self):
        inputs = [[[ord('3')],[ord('+')],[ord('3')]],
                  [[ord('(')],[ord('3')],[ord('+')],[ord('3')],[ord(')')]],
                  [[ord('(')],[ord('m'),ord('i'),ord('n')],[ord('(')],[ord('1')],[ord(',')],[ord('2')],[ord(')')],[ord(')')]],
                  [[ord('s'),ord('i'),ord('n')],[ord('(')],[ord('3')],[ord(')')]]]
        results = [self.validator.missing_function(input) for input in inputs]
        self.assertEqual(results, [""]*len(results))
