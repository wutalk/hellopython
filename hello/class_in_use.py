class Complex:
    clazz_var = 'class variable 1'

    def __init__(self, name, age):
        self.name = name
        self.age = age  # age and name are object variables


x = Complex('owen', 22)
print Complex.clazz_var
print x.name, x.age

x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print x.counter

del x.counter


# print x.counter # will result AttributeError: Complex instance has no attribute 'counter'

class Simple(Complex):
    def __init__(self, name):
        self.name = name


s = Simple('simple')
print s.clazz_var  # inherit
print s.name  # override
print isinstance(s, Complex)


# 9.8. Exceptions Are Classes Too
class B:
    pass


class C(B):
    pass


class D(C):
    pass


for c in [B, C, D]:
    try:
        raise c()
    except D:
        print 'D'
    except C:
        print 'C'
    except B:
        print 'B'

print sum(x + y for x, y in zip([1, 2, 3], [4, 5, 6]))

sum = 0
for x, y in zip([1, 2, 3], [4, 5, 6]):
    sum = sum + x + y
print sum

