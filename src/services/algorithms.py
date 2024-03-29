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
                            'pi': math.pi, 'sqrt': math.sqrt}
        self._operands_no = {'+': 2, '-': 2, '*': 2, '/': 2, '^': 2, 'sin': 1, 'cos': 1, 'tan': 1, 'max': 2, 'min': 2,
                             'ln': 1, 'log': 1, 'pi': 0, 'sqrt': 1}

        self.variables = None
        self.input_chars = None
        self.input_ints = None
        self.input_elements = None
        self.input_elements_in_postfix = None
        self.input_values_in_postfix = None
        self.result = None

    def set_input(self, input_chars, variables):
        self.input_chars = input_chars
        self.input_ints = self.string_to_unicode_code_point_integers()
        self.input_elements = self.input_int_list_to_input_element_list()
        self.variables = variables
        self.input_elements_in_postfix = self.shunting_yard()
        self.unicode_code_point_integers_to_values()

    def string_to_unicode_code_point_integers(self) -> list[int]:
        """Changes a string of characters into a list of the unicode
        code point integers of the characters
        """

        output = []
        for char in self.input_chars:
            output.append(ord(char))
        return output

    def input_int_list_to_input_element_list(self) -> list[int]:
        """Checks which unicode point integers are part of a number, function name and saves them in
        the output list as a list of integers. Other allowed characters' unicode point integers are
        stored as they are in the output list
        """

        output = []
        current = []
        for element in self.input_ints:
            if element in self._possible_variables or element in self._operators + [self._left_bracket, self._right_bracket] or element is self._comma:
                if current:
                    output.append(current)
                    current = []
                output.append([element])
            elif element in self._numbers or element is self._dot:
                if (current and ((current[-1] not in self._numbers) and (current[-1] != self._dot))):
                    output.append(current)
                    current = []
                current.append(element)
            elif element in self._alphabets:
                if current and current[-1] not in self._alphabets:
                    output.append(current)
                    current = []
                current.append(element)
            else:
                return []
        if current:
            output.append(current)

        return output

    def shunting_yard(self) -> deque:
        """Converts input from infix to postfix notation
        """

        output = deque()
        operators = deque()
        precedence = {ord('+'): 1, ord('-'):1, ord('*'): 2, ord('/'): 2, ord('^'): 3}
        left_associative = {ord('+'): True, ord('-'): True, ord('*'): True, ord('/'): True, ord('^'): False}

        for element in self.input_elements:
            if element[0] in self._numbers or chr(element[0]) in self.variables.keys():
                output.append(element)
            elif element[0] in self._alphabets:
                operators.append(element)
            elif element[0] in self._operators:
                while operators and (operators[-1][0] is not self._left_bracket) and ((precedence.get(operators[-1][0]) > precedence.get(element[0])) or (precedence.get(operators[-1][0]) == precedence.get(element[0]) and left_associative.get(element[0]))):
                    output.append(operators.pop())
                operators.append(element)
            elif element[0] is self._comma:
                while operators and (operators[-1][0] is not self._left_bracket):
                    output.append(operators.pop())
            elif element[0] is self._left_bracket:
                operators.append(element)
            elif element[0] is self._right_bracket:
                while operators and operators[-1][0] is not self._left_bracket:
                    output.append(operators.pop())
                if operators and operators[-1][0] is self._left_bracket:
                    operators.pop()
                else:
                    return []
                if operators and operators[-1][0] in self._alphabets:
                    output.append(operators.pop())
        while len(operators) > 0:
            if operators[-1][0] is self._left_bracket:
                return []
            output.append(operators.pop())

        return output

    def set_precision(self) -> int:
        """ Goes through the input list and returns the smallest number decimal places"""

        decimal_places = 0
        min_decimal_places = None
        dot_found = False
        for element in self.input_elements:
            for number in element:
                if dot_found:
                    decimal_places += 1
                if number is self._dot:
                    dot_found = True
            if dot_found:
                if min_decimal_places == None or decimal_places < min_decimal_places:
                    min_decimal_places = decimal_places
                dot_found = False
        
        if decimal_places == 0:
            self.result = int(self.result)
        else:
            self.result = round(self.result, decimal_places)


    def unicode_code_point_integers_to_values(self) -> deque:
        """Converts a list of lists of unicode point integers into strings (operators and functions)
        or floats (numbers)"""

        output = deque()
        current = ""
        for element in self.input_elements_in_postfix:
            for number in element:
                current += chr(number)
            if element[0] in self._numbers:
                output.append(float(current))
            elif element[0] in self._possible_variables:
                output.append(self.variables.get(current))
            else:
                output.append(current)
            current = ""
        self.input_values_in_postfix = output

    def evaluate_input_in_postfix_notation(self) -> float:
        """Evaluates the input string in postfix notation and stores the result in self.result"""

        temp = deque()
        while self.input_values_in_postfix:
            current = self.input_values_in_postfix.popleft()
            if operation := self._operations.get(current):
                arguments = []
                for i in range(self._operands_no.get(current)):
                    arguments.append(temp.pop())
                temp.append(operation(*arguments))
            else:
                temp.append(current)
        self.result = temp.pop()

    def calculate_result(self):
        self.evaluate_input_in_postfix_notation()
        self.set_precision()
