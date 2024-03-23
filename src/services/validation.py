def incorrect_brackets(unvalidated_input: list[int]) -> bool:
    """Checks whether the input list contains unicode point integers for '(' and ')'
    in incorrect order

    Args:
        unvalidated_input (list[int]): list of unicode point integers of the input string

    Returns:
        bool: whether incorrect usage of brackets was found
    """

    open_brackets = 0
    left = ord("(")
    right = ord(")")
    for char in unvalidated_input:
        if open_brackets < 0:
            return True
        elif char == left:
            open_brackets += 1
        elif char == right:
            open_brackets -= 1
    return open_brackets != 0

def unassigned_variables(values: list[int], possible_vars: range, vars: range) -> bool:
    """Checks whether input list of unicode point integers contains integers for unassigned variables
    which are to a dictionary where keys are capital letters from A to Z

    Args:
        values (list[int]): list of unicode point integers of the input string
        possible_vars (range): range of unicode point integers from A to Z
        vars (range): range of unicode point integers of assigned variables

    Returns:
        bool: whether unassigned variables were found
    """
    
    for value in values:
        if value in possible_vars:
            if value not in vars:
                return True
    return False

def improper_operator_use(unvalidated_input: list[int], operators: list[int]) -> bool:
    """Checks whether input list of unicode point integers contains operators as the first or last character
    of the input or whether there are two adjacent operators

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
