from math import pi

# List [ ... ]
# Kiwi QiYiGuo/MiHouTao, dragonfruit HuoLongGuo, loquats PiPa, lychee LiZhi,Pomelo YouZi
fruits = ['kiwi', 'dragon fruit', 'loquats', 'lychee', 'Pomelo']
print(fruits)
fruits.append('apple')
print(fruits)

biggerFruits = []
biggerFruits.extend(fruits)
print(biggerFruits)

fruits.remove('apple')
fruits.append('kiwi')
print(fruits)
# Set set([ ... ])

print('lychee' in set(fruits))
print(fruits.count('kiwi'))

for i in range(1, 10):
    print(str(round(pi, i))),
print()

# tuple ( .. )
tuple = 128, 256, 512
print(tuple)

# dictionary { ... }
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
print(tel)

print(tel['sape'])
print('jack in key', 'jack' in tel.keys())

for i, v in tel.iteritems():
    print i, v

print('hello {}!'.format('owen'))

def divide(x,y):
    try:
        result = x/y
    except ZeroDivisionError:
        print('division by zero')
    else:
        print("result is {}".format(result))
    finally:
        print('in finally')

divide(1,2)
divide(1,0)