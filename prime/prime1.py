from sympy import sieve


p = list(sieve.primerange(1, 10**6))
print(f'{p=} total={len(p)}')
