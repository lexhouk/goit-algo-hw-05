from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    '''
    Prepare cache for Fibonacci's numbers.

    :return: Callable[[int], int]
    '''

    cache: dict[int, int] = {}

    def fibonacci(number: int) -> int:
        '''
        Calculate Fibonacci's number and read proceed numbers from the cache.

        :param number: int

        :return: int
        '''

        if number not in cache:
            if number < 1:
                cache[number] = 0
            elif number > 1:
                cache[number] = fibonacci(number - 1) + fibonacci(number - 2)
            else:
                cache[number] = 1

        return cache[number]

    return fibonacci
