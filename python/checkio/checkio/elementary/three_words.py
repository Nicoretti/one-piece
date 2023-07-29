#!/usr/bin/env python3
"""
Let's teach the Robots to distinguish words and numbers.
You are given a string with words and numbers separated by whitespaces (one space). The words contains only letters.
You should check if the string contains three words in succession. For example, the string "start 5 one two three 7 end"
contains three words in succession.

Input: A string with words.
Output: The answer as a boolean.
Precondition: The input contains words and/or numbers. There are no mixed words (letters and digits combined).
0 < len(words) < 100
"""


def is_word(string):
    return not string.isdigit()


def checkio(words):
    words = words.split(" ")
    found_in_succession = 0
    if len(words) < 3:
        return False
    for word in words:
        if is_word(word):
            found_in_succession += 1
            if found_in_succession >= 3:
                return True
        else:
            found_in_succession = 0
    return False


if __name__ == '__main__':
    assert checkio("Hello World hello") == True, "Hello"
    assert checkio("He is 123 man") == False, "123 man"
    assert checkio("1 2 3 4") == False, "Digits"
    assert checkio("bla bla bla bla") == True, "Bla Bla"
    assert checkio("Hi") == False, "Hi"

