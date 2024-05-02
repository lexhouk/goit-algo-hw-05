from re import search
from typing import Callable, Generator
from decimal import Decimal, ROUND_HALF_EVEN as ROUND


def generator_numbers(text: str) -> Generator[Decimal, None, None]:
    '''
    Extract all floating point numbers from plain text where the first ones are
    separated by spaces.

    :param text: str

    :return: Generator[Decimal, None, None]
    '''

    while number := search(r'\s+(\d+(|\.\d+))\s+', text):
        yield Decimal(number.group()).quantize(Decimal('0.00'), ROUND)

        text = text[number.end():]


def sum_profit(
    text: str,
    func: Callable[[str], Generator[Decimal, None, None]]
) -> Decimal:
    '''
    Add all the numbers obtained from the given function.

    :param text: str
    :param func: Callable[[str], Generator[Decimal, None, None]]

    :return: Decimal
    '''

    return sum(func(text))
