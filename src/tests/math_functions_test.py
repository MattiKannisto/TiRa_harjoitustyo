import unittest

from services import math_functions

class TestValidation(unittest.TestCase):
    def test_addition_works_with_positive_and_negative_numbers(self):
        inputs = [[1,2], [-5,3], [-6,-2], [0,0], [134324324,0]]
        results = []
        for input in inputs:
            results.append(math_functions.add(*input))

        self.assertEqual(results, [1+2, (-5)+3, (-6)+(-2), 0+0, 134324324+0])
