from collections import deque


def string_to_unicode_code_point_integers(input: str) -> list[int]:
    """Changes a string of characters into a list of the unicode
    code point integers of the characters

    Args:
        input (str): input as a string of characters

    Returns:
        list[int]: input as a list of unicode code point integers
    """

    output = []
    for char in input:
        output.append(ord(char))
    return output

def input_int_list_to_input_element_list(input: list[int], alphabets: range, variables: range,
                                         numbers: range, single_chars: list[int], dot: int,
                                         operators: list[int], space: int) -> list[int]:
    """Checks which unicode point integers are part of a number, function name and saves them in
    the output list as a list of integers. Other allowed characters' unicode point integers are
    stored as they are in the output list

    Args:
        input (list[int]): list of unicode point integers of the input string
        alphabets (range): list of unicode point integers of alphabets from a to z
        variables (range): list of unicode point integers of alphabets from A to Z
        numbers (range): list of unicode point integers of numbers from 0 to 9
        left_bracket (int): unicode point integer of '('
        right_bracket (int): unicode point integer of ')'
        dot (int): unicode point integer of '.'
        operators (list[int]): list of unicode point integers of the used operators
        space (int): unicode point integer of ' '

    Returns:
        list: list of unicode point integers of the input where numbers' and function names'
              integers are stored as lists of integers
    """
    output = []
    current = []
    for element in input:
        if element in variables or element in operators + single_chars:
            if current:
                output.append(current)
                current = []
            if element is not space:
                output.append([element])
        elif element in numbers or element is dot:
            if (current and ((current[-1] not in numbers) and (current[-1] != dot))):
                output.append(current)
                current = []
            current.append(element)
        elif element in alphabets:
            if current and current[-1] not in alphabets:
                output.append(current)
                current = []
            current.append(element)
        else:
            return []
    if current:
        output.append(current)

    return output

def shunting_yard(validated_input: list[list[int]], alphabets: range, numbers: range,
                  left_bracket: int, right_bracket: int, used_operators: list[int],
                  variables: dict) -> deque:
    """Converts input from infix to postfix notation

    Args:
        validated_input (list[list[int]]): input in infix notation
        alphabets (range): alphabets' unicode point integer range
        numbers (range): numbers' unicode point integer range
        left_bracket (int): left bracket's unicode point integer
        right_bracket (int): right bracket's unicode point integer
        used_operators (list[int]): unicode point integers of operators used

    Returns:
        list: input in postfix notation
    """

    output = deque()
    operators = deque()
    precedence = {ord('+'): 1, ord('-'):1, ord('*'): 2, ord('/'): 2, ord('^'): 3}
    left_associative = {ord('+'): True, ord('-'): True, ord('*'): True, ord('/'): True, ord('^'): False}

    for element in validated_input:
        if element[0] in numbers or chr(element[0]) in variables.keys():
            output.append(element)
        elif element[0] in alphabets:
            operators.append(element)
        elif element[0] in used_operators:
            while operators and (operators[-1][0] is not left_bracket) and (precedence.get(operators[-1][0]) > precedence.get(element[0]) or (precedence.get(operators[-1][0]) == precedence.get(element[0]) and left_associative.get(element[0]))):
                output.append(operators.pop())
            operators.append(element)
        elif element[0] is left_bracket:
            operators.append(element)
        elif element[0] is right_bracket:
            while operators and operators[-1][0] is not left_bracket:
                output.append(operators.pop())
            if operators and operators[-1][0] is left_bracket:
                operators.pop()
            else:
                return []
            if operators and operators[-1][0] in alphabets:
                output.append(operators.pop())

    while len(operators) > 0:
        if operators[-1][0] is left_bracket:
            return []
        output.append(operators.pop())

    return output

def get_min_number_of_decimal_places(input_list: list[list[int]], dot: int) -> int:
    """ Goes through the input list and returns the smallest number decimal places

    Args:
        input_list (list[list[int]]): unicode point integers
        numbers (range): numbers' unicode point integer range
        dot (int): dot's unicode point integer

    Returns:
        int: smallest number of decimal places found
    """

    decimal_places = 0
    min_decimal_places = None
    dot_found = False
    for element in input_list:
        for number in element:
            if dot_found:
                decimal_places += 1
            if number is dot:
                dot_found = True
        if dot_found:
            if min_decimal_places == None or decimal_places < min_decimal_places:
                min_decimal_places = decimal_places
            dot_found = False
    return min_decimal_places

def unicode_code_point_integers_to_values(input_list: list[list[int]], numbers: range,
                                          variable_chars: range, variables: dict) -> deque:
    """Converts a list of lists of unicode point integers into strings (operators and functions)
    or floats (numbers)

    Args:
        input_list (list[list[int]]): unicode point integers
        numbers (range): numbers' unicode point integer range
        variable_chars (range): variable characters unicode point integer range
        variables (dict): variables

    Returns:
        deque: input converted to strings or floats
    """

    output = deque()
    current = ""
    for element in input_list:
        for number in element:
            current += chr(number)
        if element[0] in numbers:
            output.append(float(current))
        elif element[0] in variable_chars:
            output.append(variables.get(current))
        else:
            output.append(current)
        current = ""
    return output


def evaluate_input_in_postfix_notation(postfix_input: deque, operations: dict, operands_no: dict) -> float:
    """Evaluates the input string in postfix notation and returns the result as a float

    Args:
        postfix_input (deque): input in postfix notation
        operations (dict): operators mapped to corresponding functions
        operands_no (dict): numbers of operands needed by functions corresponding to operators

    Returns:
        float: result from evaluation of input in postfix notation
    """

    temp = deque()
    while postfix_input:
        current = postfix_input.popleft()
        if operation := operations.get(current):
            first = temp.pop()
            if operands_no.get(current) == 2:
                second = temp.pop()
                result = operation(first,second)
            else:
                result = operation(first)
            temp.append(result)
        else:
            temp.append(current)
    return temp.pop()