#!/usr/bin/env python3
"""
You are given an array with positive numbers and a number N. You should find the N-th power of the element in the array
with the index N. If N is outside of the array, then return -1. Don't forget that the first element has the index 0.
Let's look at a few examples:
- array = [1, 2, 3, 4] and N = 2, then the result is 32 == 9;
- array = [1, 2, 3] and N = 3, but N is outside of the array, so the result is -1.

Input: Two arguments. An array as a list of integers and a number as a integer.
Output: The result as an integer.
Precondition: 0 < len(array) ≤ 10
0 ≤ N
all(0 ≤ x ≤ 100 for x in array)
"""


def index_power(array, n):
    """
    Find Nth power of the element with index N.
    """
    result = -1
    try:
        result = array[n] ** n
    except IndexError as ex:
        result = -1
    return result


if __name__ == '__main__':
    assert index_power([1, 2, 3, 4], 2) == 9, "Square"
    assert index_power([1, 3, 10, 100], 3) == 1000000, "Cube"
    assert index_power([0, 1], 0) == 1, "Zero power"
    assert index_power([1, 2], 3) == -1, "IndexError"
