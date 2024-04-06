import typing
from collections import deque
import math

from services import math_functions


class Calculator:

    def __init__(self):
        """_summary_"""

        self._possible_variables = range(ord('A'),ord('Z')+1)
        self._operators = [ord('+'),ord('-'),ord('*'),ord('/'),ord('^')]
        self._alphabets = range(ord('a'),ord('z')+1)
        self._left_bracket = ord('(')
        self._right_bracket = ord(')')
        self._comma = ord(',')
        self._dot = ord('.')
        self._numbers = range(ord('0'),ord('9')+1)
        self._operations = {'+': math_functions.add, '-': math_functions.subtract, '*': math_functions.multiply,
                            '/': math_functions.divide, '^': math_functions.raise_to_exponent, 'sin': math.sin,
                            'cos': math.cos, 'tan': math.tan, 'max': max, 'min': min, 'ln': math.log, 'log': math.log10,
                            'sqrt': math.sqrt}
        self._constants = {'pi': math.pi, 'e': math.e}
        self._operands_no = {'+': 2, '-': 2, '*': 2, '/': 2, '^': 2, 'sin': 1, 'cos': 1, 'tan': 1, 'max': 2, 'min': 2,
                             'ln': 1, 'log': 1, 'pi': 0, 'sqrt': 1, 'e': 0}

        self._variables = None
        self._input_chars = None
        self._input_ints = []
        self._input_values_in_postfix = deque()
        self._precision = 0
        self.input_elements = []
        self.input_elements_in_postfix = deque()
        self.result = None

    def set_input(self, input_chars: str, variables: dict, precision: int) -> None:
        self._input_chars = input_chars
        self._variables = variables
        if precision > 0:
            self._precision = precision
        else:
            self._precision = None

        self.string_to_unicode_code_point_integers()
        self.input_int_list_to_input_element_list()
        self.shunting_yard()
        self.unicode_code_point_integers_to_values()

    def string_to_unicode_code_point_integers(self) -> None:
        """Changes a string of characters into a list of the unicode
        code point integers of the characters
        """

        self._input_ints.clear()
        for char in self._input_chars:
            self._input_ints.append(ord(char))

    def input_int_list_to_input_element_list(self) -> list[list[int]]:
        """Checks which unicode point integers are part of a number, function name and saves them in
        the output list as a list of integers. Other allowed characters' unicode point integers are
        stored as they are in the output list
        """

        self.input_elements.clear()
        current = []
        for element in self._input_ints:
            if element in self._possible_variables or element in self._operators + [self._left_bracket, self._right_bracket] or element is self._comma:
                if current:
                    self.input_elements.append(current)
                    current = []
                self.input_elements.append([element])
            elif element in self._numbers or element is self._dot:
                if (current and ((current[-1] not in self._numbers) and (current[-1] != self._dot))):
                    self.input_elements.append(current)
                    current = []
                current.append(element)
            elif element in self._alphabets:
                if current and current[-1] not in self._alphabets:
                    self.input_elements.append(current)
                    current = []
                current.append(element)
            else:
                return []
        if current:
            self.input_elements.append(current)

    def shunting_yard(self) -> deque:
        """Converts input from infix to postfix notation
        """

        self.input_elements_in_postfix.clear()
        operators = deque()
        precedence = {ord('+'): 1, ord('-'):1, ord('*'): 2, ord('/'): 2, ord('^'): 3}
        left_associative = {ord('+'): True, ord('-'): True, ord('*'): True, ord('/'): True, ord('^'): False}

        for element in self.input_elements:
            if element[0] in self._numbers or chr(element[0]) in self._variables.keys():
                self.input_elements_in_postfix.append(element)
            elif element[0] in self._constants.keys():
                self.input_elements_in_postfix.append(element)
            elif element[0] in self._alphabets:
                operators.append(element)
            elif element[0] in self._operators:
                while operators and (operators[-1][0] is not self._left_bracket) and ((precedence.get(operators[-1][0]) > precedence.get(element[0])) or (precedence.get(operators[-1][0]) == precedence.get(element[0]) and left_associative.get(element[0]))):
                    self.input_elements_in_postfix.append(operators.pop())
                operators.append(element)
            elif element[0] is self._comma:
                while operators and (operators[-1][0] is not self._left_bracket):
                    self.input_elements_in_postfix.append(operators.pop())
            elif element[0] is self._left_bracket:
                operators.append(element)
            elif element[0] is self._right_bracket:
                while operators and operators[-1][0] is not self._left_bracket:
                    self.input_elements_in_postfix.append(operators.pop())
                if operators and operators[-1][0] is self._left_bracket:
                    operators.pop()
                else:
                    return self.input_elements_in_postfix.clear()
                if operators and operators[-1][0] in self._alphabets:
                    self.input_elements_in_postfix.append(operators.pop())

        while len(operators) > 0:
            if operators[-1][0] is self._left_bracket:
                return self.input_elements_in_postfix.clear()
            self.input_elements_in_postfix.append(operators.pop())

    def unicode_code_point_integers_to_values(self):
        """Converts a list of lists of unicode point integers into strings (operators and functions)
        or floats (numbers)"""

        current = ""
        for element in self.input_elements_in_postfix:
            for number in element:
                current += chr(number)
            if element[0] in self._numbers:
                self._input_values_in_postfix.append(float(current))
            elif current in self._constants.keys():
                self._input_values_in_postfix.append(self._constants.get(current))
            elif element[0] in self._possible_variables:
                self._input_values_in_postfix.append(self._variables.get(current))
            else:
                self._input_values_in_postfix.append(current)
            current = ""

    def evaluate_input_in_postfix_notation(self):
        """Evaluates the input string in postfix notation and stores the result in self.result"""

        temp = deque()
        while self._input_values_in_postfix:
            current = self._input_values_in_postfix.popleft()
            if operation := self._operations.get(current):
                arguments = []
                for i in range(self._operands_no.get(current)):
                    arguments.append(temp.pop())
                temp.append(operation(*arguments))
            else:
                temp.append(current)
        self.result = round(temp.pop(), self._precision)
