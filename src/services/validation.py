import inspect

class Validator:
    """A glass for validating the user given input. The validator uses unicode point integers in
    validating the input. The validation functions return their own name with capitalized first
    word and an exclamation mark at the end if they find that the input is invalid, otherwise they
    return an empty string. Validator cannot detect errors such as division by zero since it
    it validates the unevaluated input. Such errors will need to be detected when the input
    is being evaluated
    """

    def __init__(self, ops: list[int], fns: list[list[int]], ranges: dict, ints: dict):
        """A constructor for a Validator object

        Args:
            ops (list[int]): used operators unicode point integers
            fns (list[list[int]]): used functions unicode point integers in lists
            ranges (dict): ranges of unicode point integers of numbers, variables and function names
            ints (dict): unicode point integers of brackets, comma and dot
        """

        self._ops = ops
        self._fns = fns
        self._ranges = ranges
        self._ints = ints

    def get_errors(self, tokens: list[list[int]], vars_in_use: dict, tokens_in_postfix: list[list[int]]) -> str:
        """Calls all validation functions and stores their return values (function's own name or
        empty string) in a list. Either the first nonempty string of this list or an empty string
        will be returned

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens
            vars_in_use (dict): variables used to store previous results
            tokens_in_postfix (list[list[int]]): lists of unicode point integers of the input
                                                   tokens in postfix

        Returns:
            str: an error message or an empty string
        """

        error_messages = [self.unassigned_variables_used(tokens, vars_in_use),
                          self.invalid_use_of_operators(tokens),
                          self.unknown_function_used(tokens),
                          self.missing_operator(tokens),
                          self.invalid_use_of_dot(tokens),
                          self.invalid_use_of_functions(tokens),
                          self.missing_function_argument(tokens),
                          self.mismatched_parentheses(tokens_in_postfix)]

        return next((message for message in error_messages if message), "")

    def get_calling_function_name(self) -> str:
        """Gets the calling function name, replaces underscores with spaces and capitalizes
        the first letter

        Returns:
            str: calling function name capitalized and underscores replaced with spaces
        """

        name = inspect.stack()[1][3]
        return name.replace("_", " ").capitalize() + "!"

    def unassigned_variables_used(self, tokens: list[list[int]], vars_in_use: dict) -> str:
        """Checks whether input list of lists of unicode point integers contains integers
        for unassigned variables. Variables in the dict have keys starting from 'A' to
        the max of 'Z'

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens
            vars_in_use (dict): variables used to store previous results

        Returns:
            str: function name or empty string
        """

        unassigned_vars_ints = range(ord('A') + len(vars_in_use.keys()), ord('Z')+1)
        for token in tokens:
            if token[0] in unassigned_vars_ints:
                return self.get_calling_function_name()
        return ""

    def invalid_use_of_operators(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains operators as
        the first or last character of the input or whether there are two or more adjacent operators

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        brackets = [self._ints['('], self._ints[')']]
        if tokens[0][0] in self._ops or tokens[-1][0] in self._ops:
            return self.get_calling_function_name()
        for i in range(len(tokens)):
            curr = tokens[i][0]
            if curr in self._ops:
                prev = tokens[i-1][0]
                nxt = tokens[i+1][0]
                two_adjacent_ops = nxt in self._ops
                op_adjacent_to_bracket = any(map(lambda e: e in [prev, nxt], brackets))
                if two_adjacent_ops or op_adjacent_to_bracket:
                    return self.get_calling_function_name()
        return ""

    def missing_operator(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers is missing an operator

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        for i in range(len(tokens)-1):
            curr = tokens[i][0]
            nxt = tokens[i+1][0]
            cant_be_adjacent = [self._ranges['a_to_z'],self._ranges['A_to_Z'],self._ranges['0_to_9']]
            num_or_var = [self._ranges['A_to_Z'],self._ranges['0_to_9']]
            no_op_before_l_bracket = any(curr in x for x in num_or_var) and nxt is self._ints['(']
            no_op_after_r_bracket = curr is self._ints[')'] and any(nxt in n for n in cant_be_adjacent)
            if any([any(curr in x for x in cant_be_adjacent) and any(nxt in n for n in cant_be_adjacent),
                    no_op_before_l_bracket, no_op_after_r_bracket]):
                return self.get_calling_function_name()
        return ""

    def unknown_function_used(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains lowercase
        alphabets that do not correspond to any of the functions used

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        for token in tokens:
            if token[0] in self._ranges['a_to_z'] and not token in self._fns:
                return self.get_calling_function_name()
        return ""

    def invalid_use_of_dot(self, tokens) -> bool:
        """Checks whether input list of lists of unicode point integers contains a lone dot

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        return ([self._ints['.']] in tokens)*self.get_calling_function_name() or ""

    def invalid_use_of_functions(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains functions
        with incorrect number of arguments

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        for i in range(len(tokens)):
            if tokens[i][0] in self._ranges['a_to_z']:
                brackets = 0
                commas = 0
                for j in range(i+1,len(tokens)):
                    if brackets == 1 and tokens[j][0] is self._ints[',']:
                        commas += 1
                    if tokens[j][0] is self._ints['(']:
                        brackets += 1
                    elif tokens[j][0] is self._ints[')']:
                        brackets -= 1
                    if brackets <= 0:
                        break
                if commas != 0 + 1*(tokens[i][0] == ord('m')):
                    return self.get_calling_function_name()
        return ""


    def missing_function_argument(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers contains functions
        missing arguments

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        for i in range(len(tokens)):
            if tokens[i][0] is self._ints['('] and tokens[i+1][0] in [self._ints[','], self._ints[')']]:
                return self.get_calling_function_name()
            if tokens[i][0] is self._ints[','] and tokens[i+1][0] is self._ints[')']:
                return self.get_calling_function_name()
        return ""

    def mismatched_parentheses(self, tokens: list[list[int]]) -> str:
        """Checks whether input list of lists of unicode point integers is an empty list. Shunting
        yard algorithm produces such a list in case of mismatched parentheses in the input

        Args:
            tokens (list[list[int]]): lists of unicode point integers of the input tokens

        Returns:
            str: function name or empty string
        """

        return (not tokens)*self.get_calling_function_name() or ""
