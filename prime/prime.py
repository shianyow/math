import math


def f1():
    prime = [2]

    for i in range(3, 1000000, 2):
        s = math.sqrt(i)
        for p in prime:
            if p > s:
                prime.append(i)
                break
            if i % p == 0:
                break

    return prime


p1 = f1()
print(f'{p1=} total={len(p1)}')
