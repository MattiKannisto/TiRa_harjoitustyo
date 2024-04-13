import unittest
import math
from collections import deque

from services import algorithms

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = algorithms.Calculator()

    def test_input_string_is_converted_to_integers_correctly(self):
        self.assertEqual(self.calculator.chars_to_ints("1+2*3-4"), [ord('1'),ord('+'),ord('2'),ord('*'),ord('3'),ord('-'),ord('4')])

    def test_input_integers_are_converted_to_input_tokens_correctly(self):
        input = [ord('1'),ord('2'),ord('+'),ord('s'),ord('i'),ord('n'),ord('('),ord('3'),ord(')'),ord('*'),ord('3')]
        result = self.calculator.ints_to_tokens(input)
        self.assertEqual(result, [[ord('1'),ord('2')],[ord('+')],[ord('s'),ord('i'),ord('n')],[ord('(')],[ord('3')],[ord(')')],[ord('*')],[ord('3')]])

    def test_operators_work_by_themselves(self):
        inputs = ["1+1", "1-1", "2*3", "4/2", "2^2"]
        outputs = []
        for input in inputs:
            self.calculator.calculate(input, {}, 0)
            outputs.append(self.calculator.result)
        self.assertEqual(outputs, [1+1, 1-1, 2*3, 4/2, 2**2])

    def test_functions_work_by_themselves(self):
        inputs = ["sin(0)", "cos(0)", "tan(0)", "max(1,2)", "min(1,2)", "ln(2)", "log(2)", "pi", "e", "sqrt(4)"]
        outputs = []
        for input in inputs:
            self.calculator.calculate(input, {}, 1)
            outputs.append(self.calculator.result)
        self.assertEqual(outputs, [round(math.sin(0),1), round(math.cos(0),1), round(math.tan(0),1), round(max(1,2),1), round(min(1,2),1), round(math.log(2),1), round(math.log10(2),1), round(math.pi,1), round(math.e,1), round(math.sqrt(4),1)])

    def test_operator_precedences_are_correct(self):
        inputs = ["3-3*2+1", "3-3/2+1", "3*2^2"]
        outputs = []
        for input in inputs:
            self.calculator.calculate(input, {}, 0)
            outputs.append(self.calculator.result)
        self.assertEqual(outputs, [3-3*2+1, int(3-3/2+1), 3*2**2])

    def test_shunting_yard_returns_empty_list_when_brackets_are_unmatched(self):
        calc = [[ord('1')],[ord('2')],[ord('+')]]
        inputs = [[[ord('(')]]+calc, [[ord(')')]]+calc+[[ord(')')]], [[ord('(')]]+calc+[[ord('(')]], calc+[[ord(')')]]]
        outputs = []
        for input in inputs:
            outputs.append(self.calculator.shunting_yard(input))
        self.assertEqual(outputs, [deque([]), deque([]), deque([]), deque([])])

    def test_result_is_has_appropriate_precision(self):
        outputs = []
        for i in range(11):
            self.calculator.calculate("pi", {}, i)
            outputs.append(self.calculator.result)
        self.assertEqual(outputs, [3, 3.1, 3.14, 3.142, 3.1416, 3.14159, 3.141593, 3.1415927, 3.14159265, 3.141592654, 3.1415926536])
