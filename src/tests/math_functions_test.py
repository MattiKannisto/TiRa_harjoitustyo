import unittest
from decimal import Decimal, getcontext

from services import math_functions

class TestMathFunctions(unittest.TestCase):
    def setUp(self):
        getcontext().prec = 10000000
        self.inputs = [[Decimal(1),Decimal(2)], [Decimal(-5),Decimal(3)], [Decimal(-6),Decimal(-2)], [Decimal(1),Decimal(0)], [Decimal(134324324),Decimal(0)], [Decimal(1111111111111111111111111111111111111111111111111),Decimal(11111111111111111111111111111111111111111111111111111)]]

    def test_addition_works_with_positive_and_negative_numbers(self):
        test_results = [math_functions.add(*input) for input in self.inputs]
        expected_results = [y+x for [x,y] in self.inputs]

        self.assertEqual(test_results, expected_results)

    def test_addition_returns_nan_when_addition_fails(self):
        self.assertEqual(math_functions.add("NaN", Decimal(3)).is_nan(), Decimal('NaN').is_nan())

    def test_subtraction_works_with_positive_and_negative_numbers(self):
        test_results = [math_functions.subtract(*input) for input in self.inputs]
        expected_results = [y-x for [x,y] in self.inputs]

        self.assertEqual(test_results, expected_results)

    def test_subtraction_returns_nan_when_subtraction_fails(self):
        self.assertEqual(math_functions.subtract("NaN", Decimal(3)).is_nan(), Decimal('NaN').is_nan())

    def test_multiplication_works_with_positive_and_negative_numbers(self):
        test_results = [math_functions.multiply(*input) for input in self.inputs]
        expected_results = [y*x for [x,y] in self.inputs]

        self.assertEqual(test_results, expected_results)

    def test_multiplication_returns_nan_when_multiplication_fails(self):
        self.assertEqual(math_functions.multiply("NaN", Decimal(3)).is_nan(), Decimal('NaN').is_nan())

    def test_division_works_with_positive_and_negative_numbers(self):
        test_results = [math_functions.divide(*input) for input in self.inputs]
        expected_results = [y/x for [x,y] in self.inputs]

        self.assertEqual(test_results, expected_results)

    def test_division_returns_nan_when_dividing_by_zero(self):
        self.assertEqual(math_functions.divide(Decimal(0), Decimal(3)).is_nan(), Decimal('NaN').is_nan())

    def test_division_returns_nan_when_division_fails(self):
        self.assertEqual(math_functions.divide("NaN", Decimal(3)).is_nan(), Decimal('NaN').is_nan())

    def test_raising_to_exponent_works_with_positive_and_negative_numbers(self):
        test_results = [math_functions.raise_to_exponent(*input) for input in self.inputs]
        expected_results = [y**x for [x,y] in self.inputs]

        self.assertEqual(test_results, expected_results)

    def test_raising_to_exponent_returns_nan_when_raising_to_exponent_fails(self):
        self.assertEqual(math_functions.raise_to_exponent("NaN", Decimal(3)).is_nan(), Decimal('NaN').is_nan())
