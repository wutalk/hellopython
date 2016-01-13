# Defining Functions
def fibonacci(n=50):  # write Fibonacci series up to n
    """Print a Fibonacci series up to n. Only 1st line of method is docstring. """
    a, b = 0, 1
    while a < n:
        print(a),
        a, b = b, a + b
    print

# global variables cannot be directly assigned a value within a function
# (unless named in a global statement), although they may be referenced.
fibonacci()
fibonacci(20)
