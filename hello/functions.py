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

# testing
def length_may_be(lst, *lens):
    length = len(lst)
    if len(lens) == 1:
        if length > int(lens[0]):
            print 'expect {0}, but received {1}'.format(lens[0], length)
    elif lens.count(str(length)) == 0:
        print ("list length {0} is not right!".format(length))
    else:
        print 'good'

molist = ['create','update']
molist.append('delete')
lens = ['1','2','4']
print(len(molist))
length_may_be(molist, '5')
