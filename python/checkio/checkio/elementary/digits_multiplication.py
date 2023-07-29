#!/usr/bin/env python3
"""
You are given a positive integer. Your function should calculate the product of the digits excluding any zeroes.
For example: The number given is 123405. The result will be 1*2*3*4*5=120 (don't forget to exclude zeroes).

Input: A positive integer.
Output: The product of the digits as an integer.
Precondition: 0 < number < 106
"""


def checkio(number):
    number_as_string = "{}".format(number)
    number = [int(digit, 10) for digit in number_as_string]
    result = 1
    for digit in number:
        if digit != 0:
            result *= digit
    return result


if __name__ == '__main__':
    assert checkio(123405) == 120
    assert checkio(999) == 729
    assert checkio(1000) == 1
    assert checkio(1111) == 1