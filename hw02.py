from re import findall
from typing import Callable, Iterable
from decimal import Decimal, ROUND_HALF_EVEN


def generator_numbers(text: str) -> Iterable[Decimal]:
    '''
    Extract all floating point numbers from plain text where the first ones are
    separated by spaces.

    :param text: str

    :return: Iterable[Decimal]
    '''

    for number in findall(r'\s+(\d+(|\.\d+))\s+', text):
        yield Decimal(number[0]).quantize(Decimal('0.00'), ROUND_HALF_EVEN)


def sum_profit(text: str, func: Callable[[str], Iterable[Decimal]]) -> Decimal:
    '''
    Add all the numbers obtained from the given function.

    :param text: str
    :param func: Callable[[str], Iterable[Decimal]]

    :return: Decimal
    '''

    return sum(func(text))
