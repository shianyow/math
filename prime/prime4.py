import math


def primes1(n):
    """ Returns  a list of primes < n """
    sieve = [True] * (n//2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]


def sundaram3(max_n):
    numbers = range(3, max_n+1, 2)
    half = (max_n)//2
    initial = 4

    for step in xrange(3, max_n+1, 2):
        for i in xrange(initial, half, step):
            numbers[i-1] = 0
        initial += 2*(step+1)

        if initial > half:
            return [2] + filter(None, numbers)


def f1():
    prime = [2]

    r = sundaram3(1000000)
    return r
    # r = range(3, 1000000, 2)
    # for i in range(3, 1000000, 2):
    for i in r:
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
