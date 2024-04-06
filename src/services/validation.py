class Validator:
    """A glass for validating the user given input
    """

    def __init__(self):
        """A constructor for a Validator object
        """

        self._possible_variables = range(ord('A'),ord('Z')+1)
        self._operators = [ord('+'),ord('-'),ord('*'),ord('/'),ord('^')]
        self._alphabets = range(ord('a'),ord('z')+1)
        self._left_bracket = ord('(')
        self._right_bracket = ord(')')
        self._comma = ord(',')
        self._dot = ord('.')

        self._input_elements = None
        self._variables = None

    def set_input(self, input_elements, variables):
        self._input_elements = input_elements
        self._variables = variables

    def unassigned_variables(self) -> bool:
        """Checks whether input list of lists of unicode point integers contains integers
        for unassigned variables. Variables in the dict have keys starting from 'A' to
        the max of 'Z'

        Returns:
            bool: whether unassigned variables were found
        """
        assigned_variables_ints = range(ord('A'),ord('A')+len(self._variables.keys()))
        for element in self._input_elements:
            if element[0] in self._possible_variables:
                if element[0] not in assigned_variables_ints:
                    return True
        return False

    def improper_operator_use(self) -> bool:
        """Checks whether input list of lists of unicode point integers contains operators as
        the first or last character of the input or whether there are two or more adjacent operators

        Returns:
            bool: whether improper operator use was found
        """

        if self._input_elements[0][0] in self._operators or self._input_elements[-1][0] in self._operators:
            return True
        for i in range(len(self._input_elements)):
            if self._input_elements[i][0] in self._operators and self._input_elements[i-1][0] in self._operators:
                return True
        return False

    def lone_dot_found(self) -> bool:
        """Checks whether input list of lists of unicode point integers contains a lone dot

        Returns:
            bool: whether a lone dot was found
        """

        return [self._dot] in self._input_elements

    def improper_function_use(self) -> bool:
        """Checks whether input list of lists of unicode point integers contains functions
        with incorrect number of arguments

        Returns:
            bool: whether a function with incorrect number of arguments was found
        """

        for i in range(len(self._input_elements)):
            if self._input_elements[i][0] in self._alphabets:
                brackets = 0
                commas = 0
                for j in range(i+1,len(self._input_elements)):
                    if brackets == 1 and self._input_elements[j][0] is self._comma:
                        commas += 1
                    if self._input_elements[j][0] is self._left_bracket:
                        brackets += 1
                    elif self._input_elements[j][0] is self._right_bracket:
                        brackets -= 1
                    if brackets <= 0:
                        break
                if self._input_elements[i][0] == ord('m') and commas != 1 or self._input_elements[i][0] != ord('m') and commas != 0:
                    return True
        return False

    def missing_function_argument(self) -> bool:
        for i in range(len(self._input_elements)):
            if self._input_elements[i][0] is self._left_bracket and self._input_elements[i+1][0] in [self._comma, self._right_bracket]:
                return True
            if self._input_elements[i][0] is self._comma and self._input_elements[i+1][0] is self._right_bracket:
                return True
        return False