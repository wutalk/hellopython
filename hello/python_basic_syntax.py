import numpy as np
import pandas as pd
import bisect
from datetime import timedelta

print("hello world")
# -*- coding: iso-8859-15 -*-

word = 'Python'
print word[0:2]
print word[:2]

squares = [1, 4, 9, 16, 25]
print(squares[:3])
squares.append(100)
print(squares)

# while Statements
a, b = 0, 1
while b < 20:
    print(b),
    a, b = b, a + b
    # t=b
    # b=a+b
    # a = t

# for Statements
words = ['cat', 'window', 'defenestrate']
for w in words:
    print w, len(w)

# if Statements
x = len(words)
if x > 5:
    print("x>5")
else:
    print("<=5")

print(range(5, 10, 2))

today = pd.datetime.today()
td = timedelta(days=365 * 5)
start = today - td

for i in range(10):
    print i
    td = timedelta(days=30 * i)
    start = today - td
    print start
