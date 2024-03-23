from collections import deque, namedtuple


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

def input_int_list_to_input_element_list(input: list[int], alphabets: range, variables: range, numbers: range,
                         left_bracket: int, right_bracket: int, dot: int, operators: list[int], space: int) -> list[int]:
    """Checks which unicode point integers are part of a number, function name and saves them in the output list as a list of integers. Other
    allowed characters' unicode point integers are stored as they are in the output list

    Args:
        input (list[int]): list of unicode point integers of the input string
        alphabets (range): list of unicode point integers of alphabets from a to z
        variables (range): list of unicode point integers of alphabets from A to Z which are used as keys for variables in a dictionary
        numbers (range): list of unicode point integers of numbers from 0 to 9
        left_bracket (int): unicode point integer of '('
        right_bracket (int): unicode point integer of ')'
        dot (int): unicode point integer of '.'
        operators (list[int]): list of unicode point integers of the used operators
        space (int): unicode point integer of ' '

    Returns:
        list: list of unicode point integers of the input where numbers' and function names' integers are stored as lists of integers
    """
    output = []
    current = []
    for element in input:
        if element in variables or element in operators or element in [space, left_bracket, right_bracket, dot]:
            if current:
                output.append(current)
                current = []
            output.append(element)
        elif element in numbers:
            if current and current[-1] not in numbers:
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

def shunting_yard(validated_input: deque, allowed_operators: list) -> list:   
    output = deque()
    operators = deque()

    for char in validated_input:
        if char in allowed_operators:
            operators.append(char)

    return output
