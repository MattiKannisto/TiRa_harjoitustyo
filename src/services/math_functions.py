def add(number_1: float, number_2: float) -> float:
    """Calculates the sum of two numbers

    Args:
        number_1 (float): first number
        number_2 (float): second number

    Returns:
        float: sum of the numbers
    """

    return number_2 + number_1

def subtract(number_1: float, number_2: float) -> float:
    """Calculates the subtraction of first number from the second number

    Args:
        number_1 (float): first number
        number_2 (float): second number

    Returns:
        float: subtraction of number 1 from number 2
    """

    return number_2 - number_1

def multiply(number_1: float, number_2: float) -> float:
    """Calculates the multiplication of two numbers

    Args:
        number_1 (float): first number
        number_2 (float): second number

    Returns:
        float: multiplication of the numbers
    """

    return number_2 * number_1

def divide(number_1: float, number_2: float) -> float | bool:
    """Calculates the division of the second number with the first number. Does
    not allow division by zero but returns None if the first number is zero

    Args:
        number_1 (float): first number
        number_2 (float): second number

    Returns:
        float: division of second number with first number if the first number is not
        zero, otherwise None
    """

    if number_1 == 0:
        return None
    return number_2 / number_1

def raise_to_exponent(number_1: float, number_2: float) -> float:
    """Calculates the second number raised to the power of the first number

    Args:
        number_1 (float): first number
        number_2 (float): second number

    Returns:
        float: second number raised to the power of the first number
    """

    return number_2 ** number_1
