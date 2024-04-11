import inspect

class Validator:
    """A glass for validating the user given input. The validator uses unicode point integers in
    validating the input. The validation functions return their own name with capitalized first
    word and an exclamation mark at the end if they find that the input is invalid, otherwise they
    return an empty string. Validator cannot detect errors such as division by zero since it
    it validates the unevaluated input. Such errors will need to be detected when the input
    is being evaluated
    """

    def __init__(self, ops: list[int], functions: list[list[int]], alphabets: range, l_bracket: int, r_bracket: int, comma: int, dot: int):
        """A constructor for a Validator object

        Args:
            ops (list[int]): used operators unicode point integers
            functions (list[list[int]]): used functions unicode point integers in lists
            alphabets (range): unicode point integers for lower case alphabets used in functions
            l_bracket (int): unicode point integer of left bracket
            r_bracket (int): unicode point integer of right bracket
            comma (int): unicode point integer of comma
            dot (int): unicode point integer of dot
        """

        self._ops = ops
        self._functions = functions
        self._alphabets = alphabets
        self._l_bracket = l_bracket
        self._r_bracket = r_bracket
        self._comma = comma
        self._dot = dot

    def get_error_message(self, elements: list[list[int]], variables: dict, elements_in_postfix: list[list[int]]) -> str:
        """Calls all validation functions and stores their return values (function own names or
        empty string) in a list. Either the first nonempty string of this list or an empty string
        will be returned

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements
            variables (dict): variables used to store previous results
            elements_in_postfix (list[list[int]]): lists of unicode point integers of the input
                                                   elements in postfix

        Returns:
            str: an error message or an empty string
        """

        error_messages = [self.unassigned_variables_used(elements, variables),
                          self.invalid_use_of_operators(elements),
                          self.unknown_function_used(elements),
                          self.missing_operator(elements),
                          self.invalid_use_of_dot(elements),
                          self.invalid_use_of_functions(elements),
                          self.missing_function_argument(elements),
                          self.mismatched_parentheses(elements_in_postfix)]

        return next((message for message in error_messages if message), "")

    def get_calling_function_name(self) -> str:
        """Gets the calling function name, replaces underscores with spaces and capitalizes
        the first letter

        Returns:
            str: Calling function name capitalized and underscores replaced with spaces
        """

        name = inspect.stack()[1][3]
        return name.replace("_", " ").capitalize() + "!"

    def unassigned_variables_used(self, elements: list[list[int]], variables: dict) -> str:
        """Checks whether input list of lists of unicode point integers contains integers
        for unassigned variables. Variables in the dict have keys starting from 'A' to
        the max of 'Z'

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements
            variables (dict): variables used to store previous results

        Returns:
            str: function name or empty string
        """

        vars = len(variables.keys())
        unassigned_variables_ints = range(ord('A') + vars, ord('Z')+1)
        for element in elements:
            if element[0] in unassigned_variables_ints:
                return self.get_calling_function_name()
        return ""

    def invalid_use_of_operators(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains operators as
        the first or last character of the input or whether there are two or more adjacent operators

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        brackets = [self._l_bracket, self._r_bracket]
        if elements[0][0] in self._ops or elements[-1][0] in self._ops:
            return self.get_calling_function_name()
        for i in range(len(elements)):
            current = elements[i][0]
            if current in self._ops:
                prev = elements[i-1][0]
                nxt = elements[i+1][0]
                two_adjacent_ops = nxt in self._ops
                op_adjavent_to_bracket = any(map(lambda e: e in [prev, nxt], brackets))
                if two_adjacent_ops or op_adjavent_to_bracket:
                    return self.get_calling_function_name()
        return ""

    def missing_operator(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers is missing an operator

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        brackets = [self._l_bracket, self._r_bracket]
        allowed = self._ops+brackets
        for i in range(len(elements)-1):
            prev = elements[i-1][0]
            current = elements[i][0]
            if i < len(elements):
                nxt = elements[i+1][0]
            if current in self._alphabets and nxt is self._l_bracket:
                continue
            if not current in allowed and not nxt in allowed or (not current in allowed and nxt is self._l_bracket) or (not current in allowed and prev is self._r_bracket):
                return self.get_calling_function_name()
        return ""

    def unknown_function_used(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains lowercase
        alphabets that do not correspond to any of the functions used

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        for element in elements:
            if element[0] in self._alphabets and not element in self._functions:
                return self.get_calling_function_name()
        return ""

    def invalid_use_of_dot(self, elements) -> bool:
        """Checks whether input list of lists of unicode point integers contains a lone dot

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        return ([self._dot] in elements)*self.get_calling_function_name() or ""

    def invalid_use_of_functions(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains functions
        with incorrect number of arguments

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        for i in range(len(elements)):
            if elements[i][0] in self._alphabets:
                brackets = 0
                commas = 0
                for j in range(i+1,len(elements)):
                    if brackets == 1 and elements[j][0] is self._comma:
                        commas += 1
                    if elements[j][0] is self._l_bracket:
                        brackets += 1
                    elif elements[j][0] is self._r_bracket:
                        brackets -= 1
                    if brackets <= 0:
                        break
                if elements[i][0] == ord('m') and commas != 1 or elements[i][0] != ord('m') and commas != 0:
                    return self.get_calling_function_name()
        return ""


    def missing_function_argument(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains functions
        missing arguments

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        for i in range(len(elements)):
            if elements[i][0] is self._l_bracket and elements[i+1][0] in [self._comma, self._r_bracket]:
                return self.get_calling_function_name()
            if elements[i][0] is self._comma and elements[i+1][0] is self._r_bracket:
                return self.get_calling_function_name()
        return ""

    def mismatched_parentheses(self, elements: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers is an empty list. Shunting
        yard algorithm produces such a list in case of mismatched parentheses in the input

        Args:
            elements (list[list[int]]): lists of unicode point integers of the input elements

        Returns:
            str: function name or empty string
        """

        return (not elements)*self.get_calling_function_name() or ""
