# This is a sample Python script.
import math

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Exercises Python Gettingstarted

# Exercise 1



print("Hello")

variabel = 5

def isItPrime(number):

    divisor = 2

    while divisor <= number / 2:
        if number % 2 == 0:
            return False
        else:
            divisor = divisor + 1

    return True

print(isItPrime(7))
print(isItPrime(125))
print(isItPrime(97))