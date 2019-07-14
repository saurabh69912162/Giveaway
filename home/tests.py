import random

a = ['a', 'b', 'c']
b = [1, 2, 3]
d = [1, 2, 3]

c = list(zip(a, b, d))

random.shuffle(c)

a, b, d = zip(*c)

print(a)
print(b)
print(d)