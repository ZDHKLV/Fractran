def crible(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[0], sieve[1] = False, False
    for start in range(2, int(limit ** 0.5) + 1):
        if sieve[start]:
            for i in range(start*start, limit + 1, start):
                sieve[i] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime]

PRIMES = crible(100000)

def prime_factors(n: int) -> list[int]:
    # heuristic: since the complete decomposition uses a crible
    # we first divide many known primes to reduce the size of our input
    # many programs were meant to only return 3^Q * P or 3^Q hence this often seals the deal
    factors = []
    for p in PRIMES:
        if n < p:
            break
        while n % p == 0:
            n //= p
            factors.append(p)

    if n > 1:
        limit = int(n**0.5) + 1
        primes = crible(limit)

        for p in primes:
            while n % p == 0:
                factors.append(p)
                n //= p

    return factors