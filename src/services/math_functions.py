from decimal import Decimal, getcontext, DivisionByZero

def add(number_1: Decimal, number_2: Decimal) -> Decimal:
    """Calculates the sum of two numbers

    Args:
        number_1 (Decimal): first number
        number_2 (Decimal): second number

    Returns:
        Decimal: sum of the numbers
    """

    try:
        return number_2 + number_1
    except:
        return Decimal('NaN')

def subtract(number_1: Decimal, number_2: Decimal) -> Decimal:
    """Calculates the subtraction of first number from the second number

    Args:
        number_1 (Decimal): first number
        number_2 (Decimal): second number

    Returns:
        Decimal: subtraction of number 1 from number 2
    """

    try:
        return number_2 - number_1
    except:
        return Decimal('NaN')

def multiply(number_1: Decimal, number_2: Decimal) -> Decimal:
    """Calculates the multiplication of two numbers

    Args:
        number_1 (Decimal): first number
        number_2 (Decimal): second number

    Returns:
        Decimal: multiplication of the numbers
    """

    try:
        return number_2 * number_1
    except:
        return Decimal('NaN')

def divide(number_1: Decimal, number_2: Decimal) -> Decimal | bool:
    """Calculates the division of the second number with the first number. Does
    not allow division by zero but returns Decimal('NaN') if the first number is zero

    Args:
        number_1 (Decimal): first number
        number_2 (Decimal): second number

    Returns:
        Decimal: division of second number with first number if the first number is not
        zero
    """
    try:
        if number_1.is_zero():
            getcontext().traps[DivisionByZero] = True
            return Decimal('NaN')
        return number_2 / number_1
    except:
        return Decimal('NaN')

def raise_to_exponent(number_1: Decimal, number_2: Decimal) -> Decimal:
    """Calculates the second number raised to the power of the first number

    Args:
        number_1 (Decimal): first number
        number_2 (Decimal): second number

    Returns:
        Decimal: second number raised to the power of the first number
    """
    try:
        return Decimal(number_2 ** number_1)
    except:
        return Decimal('NaN')