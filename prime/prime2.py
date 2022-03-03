def get_primes(n):
    numbers = set(range(n, 1, -1))
    primes = []
    while numbers:
        p = numbers.pop()
        primes.append(p)
        numbers.difference_update(set(range(p*2, n+1, p)))
    primes.sort()

    return primes


p = get_primes(1000000)
print(f'{p=} total={len(p)}')
