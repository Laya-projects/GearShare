# Base case: n is 0, producing 1. Each call reduces the problem by one with n - 1.
def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1
    return n * factorial(n - 1)


# Base case: n is 0 or 1. Each call reduces n by one, approaching one of those bases.
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


# Base case: the number is 0. Each call removes the final digit with // 10.
def sum_of_digits(number):
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return 0
    return number % 10 + sum_of_digits(number // 10)
