from collections import deque, namedtuple
import math

from services import validation, math_functions


class Calculator:
    """A class for calculating the result based on user input. The calculator uses validator class
    to validate the input before evaluating it. Zero division error can be detected only when
    the input is being evaluated and is thus detected by the function evaluating the input in
    postfix notation
    """

    def __init__(self):
        """A constructor for calculator"""

        self._possible_vars = range(ord('A'),ord('Z')+1)
        self._ops = self.chars_to_ints('+-*/^')
        self._functions = [self.chars_to_ints(x) for x in ['sin','cos','tan','max','min','ln','log','sqrt','pi','e']]
        self._alphabets = range(ord('a'),ord('z')+1)
        self._l_bracket = ord('(')
        self._r_bracket = ord(')')
        self._comma = ord(',')
        self._dot = ord('.')
        self._numbers = range(ord('0'),ord('9')+1)
        self._constants = {'pi': math.pi, 'e': math.e}

        self.result = None

        self._validator = validation.Validator(self._ops, self._functions, self._alphabets, self._l_bracket, self._r_bracket, self._comma, self._dot)

    def calculate(self, input_chars: str, vars: dict, precision: int) -> None:
        """_summary_

        Args:
            input_chars (str): the user-given input string
            vars (dict): results of previous calculations stored in a dictionary
            precision (int): user-defined precision as decimal places of the result

        Returns:
            _type_: error message, if input is invalid, otherwise input string with the result
        """

        # This is to prevent previous result from being stored in variable in case of error
        self.result = None
        # The input is converted to unicode point integers
        input_ints = self.chars_to_ints(input_chars)
        # Individual elements (e.g. numbers, function names) are put into their own lists
        input_elements = self.ints_to_elements(input_ints)
        # Input elements are converted from infix to postfix notation
        input_elements_in_postfix = self.shunting_yard(input_elements, vars)
        # Input elements are converted to corresponding values (e.g. number lists to numbers)
        values_in_postfix = self.unicode_code_point_integers_to_values(input_elements_in_postfix, vars)

        # Either an error message or empty list is received from the validator
        error_message = self._validator.get_error_message(input_elements, vars, values_in_postfix)
        if not error_message:
            # In case of zero division error, a None is returned instead of the result
            self.result = self.evaluate_input_in_postfix_notation(values_in_postfix, precision)
            if self.result is None:
                return "Cannot divide by zero!"
        return error_message or input_chars + " = " + str(self.result)

    def chars_to_ints(self, input_chars: str) -> list[int]:
        """Converts a string of characters into a list of the unicode
        code point integers of the characters

        Args:
            input_chars (str): input as a string

        Returns:
            list[int]: unicode point integers of the input string characters
        """

        return [ord(char) for char in input_chars]

    def ints_to_elements(self, input_ints: list[int]) -> list[list[int]]:
        """Checks which unicode point integers are part of a number, function name and saves them in
        the output list as a list of integers. Other allowed characters' unicode point integers are
        stored in their own lists

        Args:
            input_ints (list[int]): unicode point integers of the input string characters

        Returns:
            list[list[int]]: lists of unicode point integers of the input elements
        """

        input_elements = []
        current = []
        for element in input_ints:
            if element in self._possible_vars or element in self._ops + [self._l_bracket, self._r_bracket] or element is self._comma:
                if current:
                    input_elements.append(current)
                    current = []
                input_elements.append([element])
            elif element in self._numbers or element is self._dot:
                if (current and ((current[-1] not in self._numbers) and (current[-1] != self._dot))):
                    input_elements.append(current)
                    current = []
                current.append(element)
            elif element in self._alphabets:
                if current and current[-1] not in self._alphabets:
                    input_elements.append(current)
                    current = []
                current.append(element)
            else:
                return []
        if current:
            input_elements.append(current)
        return input_elements

    def shunting_yard(self, input_elements: list[list[int]], vars: dict) -> deque[list[int]]:
        """Converts input from infix to postfix notation. If mismatched parentheses are detected,
        an empty deque is returned

        Args:
            input_elements (list[list[int]]): lists of unicode point integers of the input elements
            vars (dict): results of previous calculations stored in a dictionary

        Returns:
            deque[list[int]]: lists of unicode point integers of the input elements in postfix notation or
                   or empty deque
        """

        input_elements_in_postfix = deque()
        ops = deque()
        precedence = {ord('+'): 1, ord('-'):1, ord('*'): 2, ord('/'): 2, ord('^'): 3}
        left_associative = {ord('+'): True, ord('-'): True, ord('*'): True, ord('/'): True, ord('^'): False}

        for element in input_elements:
            if element[0] in self._numbers or chr(element[0]) in vars.keys():
                input_elements_in_postfix.append(element)
            elif element[0] in self._constants.keys():
                input_elements_in_postfix.append(element)
            elif element[0] in self._alphabets:
                ops.append(element)
            elif element[0] in self._ops:
                while ops and (ops[-1][0] is not self._l_bracket) and ((precedence.get(ops[-1][0]) > precedence.get(element[0])) or (precedence.get(ops[-1][0]) == precedence.get(element[0]) and left_associative.get(element[0]))):
                    input_elements_in_postfix.append(ops.pop())
                ops.append(element)
            elif element[0] is self._comma:
                while ops and (ops[-1][0] is not self._l_bracket):
                    input_elements_in_postfix.append(ops.pop())
            elif element[0] is self._l_bracket:
                ops.append(element)
            elif element[0] is self._r_bracket:
                while ops and ops[-1][0] is not self._l_bracket:
                    input_elements_in_postfix.append(ops.pop())
                if ops and ops[-1][0] is self._l_bracket:
                    ops.pop()
                else:
                    return deque([])
                if ops and ops[-1][0] in self._alphabets:
                    input_elements_in_postfix.append(ops.pop())

        while len(ops) > 0:
            if ops[-1][0] is self._l_bracket:
                return deque([])
            input_elements_in_postfix.append(ops.pop())
        
        return input_elements_in_postfix

    def unicode_code_point_integers_to_values(self, elements: deque[list[int]], vars: dict) -> deque:
        """Converts a deque of lists of unicode point integers into strings (operations and functions)
        or floats (numbers)

        Args:
            elements (deque[list[int]]): lists of unicode point integers of the input elements in postfix notation or
                                         or empty deque
            vars (dict): results of previous calculations stored in a dictionary

        Returns:
            deque: strings of operations and functions or numbers as floats
        """

        values = deque()
        for element in elements:
            current = "".join(chr(number) for number in element)
            if element[0] in self._numbers:
                values.append(float(current))
            else:
                # First non-None will be appended to the values
                values.append(vars.get(current) or self._constants.get(current) or current)
        return values

    def evaluate_input_in_postfix_notation(self, values: deque, precision: int) -> float | int:
        """Evaluates the input string in postfix notation and returns it as int (if precision
        is 0) or float

        Args:
            values (deque): strings of operations and functions or numbers as floats
            precision (int): precision of the result

        Returns:
            float | int: result with correct precision
        """
        
        Function = namedtuple('Function', ['function', 'args'])
        operations = {'+': Function(math_functions.add, 2), '-': Function(math_functions.subtract, 2),
                      '*': Function(math_functions.multiply, 2), '/': Function(math_functions.divide, 2),
                      '^': Function(math_functions.raise_to_exponent, 2), 'sin': Function(math.sin, 1),
                      'cos': Function(math.cos, 1), 'tan': Function(math.tan, 1), 'max': Function(max, 2),
                      'min': Function(min, 2), 'ln': Function(math.log, 1), 'log': Function(math.log10, 1),
                      'sqrt': Function(math.sqrt, 1)}

        temp = deque()
        while values:
            current = values.popleft()
            if operation := operations.get(current):
                arguments = [temp.pop() for i in range(operation.args)]
                if result := operation.function(*arguments):
                    temp.append(result)
                else:
                    return result
            else:
                temp.append(current)

        # round() returns int if None is given as the second argument. next() returns None if none
        # of the elements in the given list are non-zero
        return round(temp.pop(), next((x for x in [precision] if x), None))
