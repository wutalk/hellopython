# List
# Kiwi QiYiGuo/MiHouTao, dragonfruit HuoLongGuo, loquats PiPa, lychee LiZhi,Pomelo YouZi
fruits = ['kiwi', 'dragonfruit', 'loquats', 'lychee', 'Pomelo']
print(fruits)
fruits.append('apple')
print(fruits)

biggerFruits = []
biggerFruits.extend(fruits)
print(biggerFruits)

fruits.remove('apple')
print(fruits)