#!/usr/bin/env python3
"""
In this mission you should write you own py3 implementation (but you can use py2 for this) of the built-in functions
min and max. Some builtin functions are closed here: import, eval, exec, globals. Don't forget you should implement two
functions in your code. max(iterable, *[, key]) or min(iterable, *[, key]) max(arg1, arg2, *args[, key])
or min(arg1, arg2, *args[, key]) Return the largest (smallest) item in an iterable or the largest(smallest) of two
or more arguments. If one positional argument is provided, it should be an iterable. The largest (smallest) item in
the iterable is returned. If two or more positional arguments are provided, the largest (smallest) of the positional
arguments is returned. The optional keyword-only key argument specifies a function of one argument that is used to
extract a comparison key from each list element (for example, key=str.lower).
If multiple items are maximal (minimal), the function returns the first one encountered.

-- Python Documentation (Built-in Functions)

Input: One positional argument as an iterable or two or more positional arguments. Optional keyword argument as a function.
Output: The largest item for the "max" function and the smallest for the "min" function.
Precondition: All test cases are correct and functions don't have to raise exceptions.
"""


def nop(param):
    return param


def lesser(lhs, rhs):
    return lhs < rhs


def greater(lhs, rhs):
    return lhs > rhs


def find(comperator, *args, **kwargs):
    key = kwargs.get("key", nop)
    it = args
    if len(args) == 1:
        it = args[0]
    result = None
    for element in it:
        if result is None:
            result = element
        if comperator(key(element), key(result)):
            result = element
    return result


def min(*args, **kwargs):
    return find(lesser, *args, **kwargs)


def max(*args, **kwargs):
    return find(greater, *args, **kwargs)


if __name__ == '__main__':
    assert max(3, 2) == 3, "Simple case max"
    assert min(3, 2) == 2, "Simple case min"
    assert max([1, 2, 0, 3, 4]) == 4, "From a list"
    assert min("hello") == "e", "From string"
    assert max(2.2, 5.6, 5.9, key=int) == 5.6, "Two maximal items"
    assert min([[1, 2], [3, 4], [9, 0]], key=lambda x: x[1]) == [9, 0], "lambda key"