def unassigned_variables(values: list[int], possible_variables: range, variables: range) -> bool:
    """Checks whether input list of unicode point integers contains integers for unassigned
    variables which are to a dictionary where keys are capital letters from A to Z

    Args:
        values (list[int]): list of unicode point integers of the input string
        possible_variables (range): range of unicode point integers from A to Z
        variables (range): range of unicode point integers of assigned variables

    Returns:
        bool: whether unassigned variables were found
    """

    for value in values:
        if value in possible_variables:
            if value not in variables:
                return True
    return False

def improper_operator_use(unvalidated_input: list[int], operators: list[int]) -> bool:
    """Checks whether input list of unicode point integers contains operators as the first
    or last character of the input or whether there are two adjacent operators

    Args:
        unvalidated_input (list[int]): list of unicode point integers of the input string
        operators (list[int]): list of unicode point integers of the used opertors

    Returns:
        bool: whether improper operator use was found
    """

    for i in range(len(unvalidated_input)):
        if unvalidated_input[i] in operators:
            if i == 0 or i == (len(unvalidated_input)-1) or unvalidated_input[i-1] in operators:
                return True
    return False

def element_in_list(input_list: list[int], element: int) -> bool:
    return element in input_list

def improper_function_use(input_list: list[int], alphabets: range, left_bracket: int,
                          right_bracket: int, numbers: range, dot: int) -> bool:
    for i in range(len(input_list)):
        if input_list[i][0] in alphabets:
            if len(input_list) - i < (3 + (input_list[i][0] == ord('m'))+1):
                return True
            j = 1
            if input_list[i+j][0] is not left_bracket:
                return True
            j += 1
            if input_list[i+j][0] not in numbers:
                return True
            if input_list[i][0] == ord('m'):
                if input_list[i+j][0] not in numbers:
                    return True
                j += 1
            j += 1
            if input_list[i+j][0] is not right_bracket:
                return True
    return False