import unittest
import math
from collections import deque
from decimal import Decimal

from services import algorithms

class TestAlgorithms(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = algorithms.Calculator()

    def test_input_string_is_converted_to_integers_correctly(self):
        self.assertEqual(self.calculator.chars_to_ints("1+2*3-4"), [ord('1'),ord('+'),ord('2'),ord('*'),ord('3'),ord('-'),ord('4')])

    def test_tokens_are_constructed_correctly_from_ints(self):
        input = [ord('3'),ord('2'),ord('.'),ord('1'),ord('0'),ord('+'),ord('A'),ord('*'),ord('7'),ord('-'),ord('s'),ord('i'),ord('n'),ord('('),ord('0'),ord(')')]
        expeceted_result = [[ord('3'),ord('2'),ord('.'),ord('1'),ord('0')],[ord('+')],[ord('A')],[ord('*')],[ord('7')],[ord('-')],[ord('s'),ord('i'),ord('n')],[ord('(')],[ord('0')],[ord(')')]]
        self.assertEqual(self.calculator.ints_to_tokens(input), expeceted_result)

    def test_shunting_yard_returns_empty_deque_when_brackets_are_unmatched(self):
        calc = [[ord('1')],[ord('2')],[ord('+')]]
        inputs = [[[ord('(')]]+calc, [[ord(')')]]+calc+[[ord(')')]], [[ord('(')]]+calc+[[ord('(')]], calc+[[ord(')')]]]
        outputs = []
        for input in inputs:
            outputs.append(self.calculator.shunting_yard(input))
        self.assertEqual(outputs, [deque([]), deque([]), deque([]), deque([])])

    def test_operators_work_by_themselves(self):
        inputs = ["1+1", "1-1", "2*3", "4/2", "2^2"]
        outputs = []
        for input in inputs:
            self.calculator.calculate(input, 0)
            outputs.append(int(self.calculator.result))
        self.assertEqual(outputs, [1+1, 1-1, 2*3, 4/2, 2**2])

    def test_functions_work_by_themselves(self):
        inputs = ["sin(0)", "cos(0)", "tan(0)", "max(1,2)", "min(1,2)", "ln(2)", "log(2)", "pi", "e", "sqrt(4)"]
        expected_values = [round(math.sin(0),1), round(math.cos(0),1), round(math.tan(0),1), round(max(1,2),1), round(min(1,2),1), round(math.log(2),2), round(math.log10(2),2), round(math.pi,1), round(math.e,1), round(math.sqrt(4),1)] # ln(2) and log(2) are rounded to 2 decimals since they are less than 0
        for i in range(len(inputs)):
            self.calculator.calculate(inputs[i], 1)
            self.assertAlmostEqual(float(self.calculator.result), expected_values[i])

    def test_operator_precedences_are_correct(self):
        inputs = ["3-3*2+1", "3-3/2+1", "3*2^2"]
        outputs = []
        for input in inputs:
            self.calculator.calculate(input, 1)
            outputs.append(float(self.calculator.result))
        self.assertEqual(outputs, [3-3*2+1, 3-3/2+1, 3*2**2])

    def test_evaluate_input_in_postfix_notation_returns_decimal_nan_when_result_is_nan(self):
        self.assertTrue(self.calculator.evaluate_input_in_postfix_notation(deque(["NaN",Decimal(3),'+']),0).is_nan())

    def test_calculate_returns_decimal_infinite_when_result_is_infinite(self):
        result = self.calculator.calculate("34325435435^32432432432",0)
        self.assertEqual(result, "Numbers too large to be computed!")

    def test_calculate_returns_correct_answer_with_simple_inputs(self):
        inputs = ["3-4*2+1", "3-4/2+1", "3*4^2", "min(3,4)*32", "min(4,3)*32", "max(3*4,4/2)"]
        outputs = []
        for input in inputs:
            outputs.append(self.calculator.calculate(input, 0))
        self.assertEqual(outputs, ["3-4*2+1 = " + str(3-4*2+1), "3-4/2+1 = " + str(3-int(4/2)+1), "3*4^2 = " + str(3*4**2), "min(3,4)*32 = " + str(3*32), "min(4,3)*32 = " + str(3*32), "max(3*4,4/2) = " + str(12)])

    def test_calculate_returns_correct_answer_with_complex_inputs(self):
        inputs = ["5*sin(max(3,2)+2)/(min(1,2))",
                  "(1*2+(pi/e)^6)-log(10)",
                  "34*A+B/(tan(3))-A*23+5*pi"]
        self.calculator.variables['A'] = Decimal(34)
        self.calculator.variables['B'] = Decimal(1)
        outputs = []
        expected_results = ["5*sin(max(3,2)+2)/(min(1,2)) = " + str(round(5*math.sin(max(3,2)+2)/(min(1,2)), 2)),
                            "(1*2+(pi/e)^6)-log(10) = " + str(round((1*2+(math.pi/math.e)**6)-math.log10(10), 2)),
                            "34*A+B/(tan(3))-A*23+5*pi = " + str(round(34*34+1/(math.tan(3))-34*23+5*math.pi, 2))]
        for input in inputs:
            outputs.append(self.calculator.calculate(input, 2))
        self.calculator.variables.clear()
        self.assertEqual(outputs, expected_results)

    def test_calculator_result_is_none_after_calculate_with_invalid_inputs(self):
        inputs = ["3-+4*2+1", "3-a/2+1", "3*4/0", "print(3)", "cos(2,4)"]
        results = []
        for input in inputs:
            self.calculator.calculate(input, 0)
            results.append(self.calculator.result)
        self.assertEqual(results, [None]*len(results))

    def test_result_has_appropriate_precision(self):
        outputs = []
        for i in range(11):
            self.calculator.calculate("pi", i)
            outputs.append(float(self.calculator.result))
        self.assertEqual(outputs, [3, 3.1, 3.14, 3.142, 3.1416, 3.14159, 3.141593, 3.1415927, 3.14159265, 3.141592654, 3.1415926536])

    def test_big_numbers_are_processed_correctly(self):
        input = "100000000000000000000000000000000000000000000000000000"
        self.calculator.calculate(input, 0)
        self.assertEqual(self.calculator.result, 100000000000000000000000000000000000000000000000000000)

    def test_big_inputs_are_processed_correctly(self):
        input = "1" + "+1"*99999
        self.calculator.calculate(input, 0)
        self.assertEqual(self.calculator.result, 100000)
