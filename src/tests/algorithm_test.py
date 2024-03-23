import unittest

from algorithms import algorithms

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_string_to_unicode_code_point_integers_returns_a_list_of_ints(self):
        non_int_found = False
        for element in algorithms.string_to_unicode_code_point_integers("ab120/&=*^_:;"):
            if not isinstance(element, int):
                non_int_found = True
                break

        self.assertAlmostEqual(non_int_found, False)