from collections import deque, namedtuple
from decimal import Decimal, getcontext
import math

from services import validation, math_functions


class Calculator:
    """A class for calculating the result based on user input. The calculator uses validator class
    to validate the input before evaluating it. Zero division error can be detected only when
    the input is being evaluated and is thus detected by the function evaluating the input in
    postfix notation. The calculator identifies different tokens based on their unicode point
    integers
    """

    def __init__(self):
        """A constructor for calculator"""

        self._ranges = {'A_to_Z': range(ord('A'),ord('Z')+1),
                        'a_to_z': range(ord('a'),ord('z')+1),
                        '0_to_9': range(ord('0'),ord('9')+1)}
        self._ints = {'(': ord('('),
                      ')': ord(')'),
                      ',': ord(','),
                      '.': ord('.')}
        self._ops = self.chars_to_ints('+-*/^')
        fn_names = ['sin','cos','tan','max','min','ln','log','sqrt','pi','e']
        self._fns = [self.chars_to_ints(x) for x in fn_names]
        self._constants = [self.chars_to_ints(x) for x in ['pi','e']]

        self.result = None
        self.variables = {}

        self._validator = validation.Validator(self._ops, self._fns, self._ranges, self._ints)

    def calculate(self, input_chars: str, precision: int) -> None:
        """Calculates the result based on the input string. If errors are detected by the
        validator class, the error message returned by the validator will be returned by
        the calculator. Otherwise the result appended to the input string will be returned

        Args:
            input_chars (str): user-given input
            precision (int): user-defined precision as decimal places of the result

        Returns:
            str: error message, if input is invalid, otherwise input string with the result
        """

        # This is to prevent previous result from being stored in variable in case of error
        self.result = None
        # This ensures big numbers can be stored in Decimals
        getcontext().prec = len(input_chars)
        # Clear error-catching traps used by Decimals
        getcontext().clear_traps()
        # The input is converted to unicode point integers
        input_ints = self.chars_to_ints(input_chars)
        # Individual tokens (e.g. numbers, function names) are put into their own lists
        tokens = self.ints_to_tokens(input_ints)
        # Input tokens are converted from infix to postfix notation
        tokens_in_postfix = self.shunting_yard(tokens)
        # Input tokens are converted to corresponding values (e.g. number lists to numbers)
        values_in_postfix = self.ints_to_values(tokens_in_postfix, self.variables)

        # Either an error message or empty string is received from the validator
        input_error = self._validator.get_input_error(tokens, self.variables, values_in_postfix)
        if not input_error:
            self.result = self.evaluate_input_in_postfix_notation(values_in_postfix, precision)
            # Results is validated for errors encountered in evaluation
            evalution_error = self._validator.get_evaluation_error(self.result)
            # Result is set to None if errors were encountered during evaluation
            if self.result.is_infinite() or self.result.is_nan():
                self.result = None
        return input_error or evalution_error or input_chars + " = " + str(self.result)

    def chars_to_ints(self, input_chars: str) -> list[int]:
        """Converts a string of characters into a list of the unicode
        code point integers of the characters

        Args:
            input_chars (str): input as a string

        Returns:
            list[int]: unicode point integers of the input string characters
        """

        return [ord(char) for char in input_chars]

    def ints_to_tokens(self, input_ints: list[int]) -> list[list[int]]:
        """Checks which unicode point integers are part of a number or function
        name and saves them in the output list as a list of integers. Other
        allowed characters' unicode point integers are stored in their own lists

        Args:
            input_ints (list[int]): unicode point integers of the input string characters

        Returns:
            list[list[int]]: lists of unicode point integers of the input tokens
        """

        tokens = []
        curr = []
        brackets = [self._ints['('], self._ints[')']]
        for input_int in input_ints:
            if input_int in self._ranges['A_to_Z'] or (
                input_int in self._ops + brackets + [self._ints[',']]):
                if curr:
                    tokens.append(curr)
                    curr = []
                tokens.append([input_int])
            elif input_int in self._ranges['0_to_9'] or input_int is self._ints['.']:
                curr.append(input_int)
            else: # input_int has to be in self._ranges['a_to_z']
                curr.append(input_int)
        if curr:
            tokens.append(curr)
        return tokens

    def shunting_yard(self, tokens: list[list[int]]) -> deque[list[int]]:
        """Converts input from infix to postfix notation. If mismatched parentheses are detected,
        an empty deque is returned

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            deque[list[int]]: lists of unicode point integers of the input tokens in postfix
                              notation or empty deque
        """

        tokens_in_postfix = deque()
        ops = deque()
        precedence = {ord('+'): 1,
                      ord('-'):1,
                      ord('*'): 2,
                      ord('/'): 2,
                      ord('^'): 3}
        left_associative = {ord('+'): True,
                            ord('-'): True,
                            ord('*'): True,
                            ord('/'): True,
                            ord('^'): False}

        for token in tokens:
            if (token[0] in self._ranges['0_to_9']) or (
                token[0] in self._ranges['A_to_Z']) or (
                token in self._constants):
                tokens_in_postfix.append(token)
            elif token[0] in self._ranges['a_to_z']:
                ops.append(token)
            elif token[0] in self._ops:
                if ops and (ops[-1][0] in self._ranges['a_to_z']):
                    precedence_1 = 4
                elif ops:
                    precedence_1 = precedence.get(ops[-1][0])
                precedence_2 = precedence.get(token[0])
                while ops and (ops[-1][0] is not self._ints['(']) and (
                    (precedence_1 > precedence_2) or (
                        precedence_1 == precedence_2 and left_associative.get(token[0]))):
                    tokens_in_postfix.append(ops.pop())
                ops.append(token)
            elif token[0] is self._ints[',']:
                while ops and (ops[-1][0] is not self._ints['(']):
                    tokens_in_postfix.append(ops.pop())
            elif token[0] is self._ints['(']:
                ops.append(token)
            else: # token[0] has to be self._ints[')'] since it is the only valid token left
                while ops and ops[-1][0] is not self._ints['(']:
                    tokens_in_postfix.append(ops.pop())
                if ops and ops[-1][0] is self._ints['(']:
                    ops.pop()
                else:
                    return deque([])
                if ops and ops[-1][0] in self._ranges['a_to_z']:
                    tokens_in_postfix.append(ops.pop())

        while len(ops) > 0:
            if ops[-1][0] is self._ints['(']:
                return deque([])
            tokens_in_postfix.append(ops.pop())

        return tokens_in_postfix

    def ints_to_values(self, tokens: deque[list[int]], vars_in_use: dict) -> deque:
        """Converts a deque of lists of unicode point integers into strings (operations and
        functions) or floats (numbers)

        Args:
            tokens (deque[list[int]]): lists of unicode point integers of the input tokens in
                                         postfix notation
            vars_in_use (dict): results of previous calculations

        Returns:
            deque: strings of operations and functions or numbers as floats
        """

        constants = {'pi': Decimal(math.pi), 'e': Decimal(math.e)}

        values = deque()
        for token in tokens:
            curr = "".join(chr(number) for number in token)
            if token[0] in self._ranges['0_to_9']:
                values.append(Decimal(curr))
            else:
                # First non-None will be appended to the values
                values.append(vars_in_use.get(curr) or constants.get(curr) or curr)
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
        operations = {'+': Function(math_functions.add, 2),
                      '-': Function(math_functions.subtract, 2),
                      '*': Function(math_functions.multiply, 2),
                      '/': Function(math_functions.divide, 2),
                      '^': Function(math_functions.raise_to_exponent, 2),
                      'sin': Function(math.sin, 1),
                      'cos': Function(math.cos, 1),
                      'tan': Function(math.tan, 1),
                      'max': Function(max, 2),
                      'min': Function(min, 2),
                      'ln': Function(math.log, 1),
                      'log': Function(math.log10, 1),
                      'sqrt': Function(math.sqrt, 1)}

        temp = deque()
        while values:
            curr = values.popleft()
            if operation := operations.get(curr):
                arguments = [temp.pop() for i in range(operation.args)]
                result = Decimal(operation.function(*arguments))
                if result.is_infinite() or result.is_nan():
                    return result
                temp.append(result)
            else:
                temp.append(curr)
        # This is needed to get the correct precision for the Decimal object
        digits = len(str(abs(int(temp[0])))) # Number of digits without a possible minus sign
        getcontext().prec = precision+digits

        # The pointless addition needed to update Decimal's precision
        return temp.pop()+Decimal(0.00000000001)-Decimal(0.00000000001)
