class Validator:

    def __init__(self):
        """_summary_
        """

        self._possible_variables = range(ord('A'),ord('Z')+1)
        self._operators = [ord('+'),ord('-'),ord('*'),ord('/'),ord('^')]
        self._alphabets = range(ord('a'),ord('z')+1)
        self._left_bracket = ord('(')
        self._right_bracket = ord(')')
        self._comma = ord(',')
        self._dot = ord('.')

    def unassigned_variables(self, values: list[int], variables: dict) -> bool:
        """Checks whether input list of unicode point integers contains integers for unassigned
        variables which are to a dictionary where keys are capital letters from A to Z

        Args:
            values (list[int]): list of unicode point integers of the input string
            variables (range): range of unicode point integers of assigned variables

        Returns:
            bool: whether unassigned variables were found
        """
        assigned_variables_ints = range(ord('A'),ord('A')+len(variables.keys()))
        for value in values:
            if value in self._possible_variables:
                if value not in assigned_variables_ints:
                    return True
        return False

    def improper_operator_use(self, unvalidated_input: list[int]) -> bool:
        """Checks whether input list of unicode point integers contains operators as the first
        or last character of the input or whether there are two adjacent operators

        Args:
            unvalidated_input (list[int]): list of unicode point integers of the input string

        Returns:
            bool: whether improper operator use was found
        """

        for i in range(len(unvalidated_input)):
            if unvalidated_input[i] in self._operators:
                if i == 0 or i == (len(unvalidated_input)-1) or unvalidated_input[i-1] in self._operators:
                    return True
        return False

    def lone_dot_found(self, input_list: list[int]) -> bool:
        return self._dot in input_list

    # def operator_missing(input: str) -> bool:
    #     first_number_found = False
    #     for char in input:
    #         if first_number_found and char == " ":
                
    #         if ord(char) in range(ord('0'),ord('9')):
    #             first_number_found = True

    def improper_function_use(self, input_list: list[int]) -> bool:
        """

        Args:
            input_list (list[int]): _description_

        Returns:
            bool: _description_
        """

        for i in range(len(input_list)):
            if input_list[i][0] in self._alphabets:
                brackets = 0
                commas = 0
                for j in range(i+1,len(input_list)):
                    if brackets == 1 and input_list[j][0] is self._comma:
                        commas += 1
                    if input_list[j][0] is self._left_bracket:
                        brackets += 1
                    elif input_list[j][0] is self._right_bracket:
                        brackets -= 1
                    if brackets <= 0:
                        break
                if input_list[i][0] == ord('m') and commas != 1 or input_list[i][0] != ord('m') and commas != 0:
                    return True
        return False