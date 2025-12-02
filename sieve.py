import time

# O(n²)
def sievev1(n: int) -> list[int]:
    primes = list(range(2, n + 1))
    for i in primes:
        for j in primes[i:]:
            if j % i == 0:
                primes.remove(j)
    return primes

# O((n²-n)/2)
def sievev2(n: int) -> list[int]:
    primes = [2] + list(range(3, n + 1, 2))
    for i in primes:
        if i == 2:
            continue
        for j in primes[i:]:
            if j % i == 0:
                primes.remove(j)
    return primes

# O(n√n/4)
def sievev3(n: int) -> list[int]:
    # O(√n/2)
    def is_primev6(n: int) -> bool:
        if n % 2 == 0 and n != 2:
            return False

        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    primes = [2]
    # O(n/2)
    for i in range(3, n + 1, 2):
        if is_primev6(i):
            primes.append(i)
    return primes


n = 100

startv1 = time.perf_counter()
primesv1 = sievev1(n)
elapsedv1 = time.perf_counter() - startv1

startv2 = time.perf_counter()
primesv2 = sievev2(n)
elapsedv2 = time.perf_counter() - startv2

startv3 = time.perf_counter()
primesv3 = sievev3(n)
elapsedv3 = time.perf_counter() - startv3

print(primesv1, round(elapsedv1, 10))
print(primesv2, round(elapsedv2, 10))
print(primesv3, round(elapsedv3, 10))
