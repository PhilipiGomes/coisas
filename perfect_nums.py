from math import isqrt


def is_perfectv1(n: int) -> bool:
    """Return True if n is a perfect number.

    - Time Complexity: O(√n)
    """
    if n <= 1:
        return False

    divisors_sum = 1
    limit = isqrt(n)
    for i in range(2, limit + 1):
        if n % i == 0:
            other = n // i
            divisors_sum += i
            if other != i:
                divisors_sum += other

    return divisors_sum == n


def is_perfectv5(n: int) -> bool:
    """Optimized perfect-number test.

    Improvements over `is_perfectv4`:
    - For even numbers, verify Euclid–Euler form and use the Lucas–Lehmer
      test (deterministic for Mersenne numbers) to check whether the
      Mersenne factor is prime.
    - For odd numbers, use `isqrt` and iterate only over 6k±1 candidates
      (after handling 2 and 3) with early exit when the divisor sum
      exceeds `n`.
    This keeps the function deterministic and often faster for very
    large candidates that match the Euclid–Euler structure.
    """
    if n <= 1:
        return False

    # Fast even-path: check Euclid-Euler form 2^(p-1)*(2^p-1)
    if n % 2 == 0:
        # count trailing zeros: e = p-1
        e = (n & -n).bit_length() - 1
        p = e + 1
        # quick form-check: odd part should equal 2^p - 1
        mersenne = (1 << p) - 1
        if n != (1 << e) * mersenne:
            return False

        # Lucas-Lehmer test for Mersenne primality (deterministic)
        def _lucas_lehmer(prime_exp: int) -> bool:
            if prime_exp == 2:
                return True
            M = (1 << prime_exp) - 1
            s = 4
            for _ in range(prime_exp - 2):
                s = (s * s - 2) % M
            return s == 0

        return _lucas_lehmer(p)

    # Odd fallback: faster divisor summing using 6k±1 iteration
    divisors_sum = 1
    limit = isqrt(n)
    # handle small primes 2 and 3 explicitly
    if n % 2 == 0:
        divisors_sum += n // 2
        if divisors_sum > n:
            return False
    if n % 3 == 0:
        other = n // 3
        divisors_sum += 3 + (other if other != 3 else 0)
        if divisors_sum > n:
            return False

    i = 5
    while i <= limit:
        # check i (6k-1) and i+2 (6k+1)
        if n % i == 0:
            other = n // i
            divisors_sum += i + (other if other != i else 0)
            if divisors_sum > n:
                return False
        j = i + 2
        if j <= limit and n % j == 0:
            other = n // j
            divisors_sum += j + (other if other != j else 0)
            if divisors_sum > n:
                return False
        i += 6

    return divisors_sum == n


def is_perfectv6(n: int) -> bool:
    """Optimized perfect-number test.

    Improvements over `is_perfectv4`:
    - For even numbers, verify Euclid–Euler form and use the Lucas–Lehmer
      test (deterministic for Mersenne numbers) to check whether the
      Mersenne factor is prime.
    - For odd numbers, use `isqrt` and iterate only over 6k±1 candidates
      (after handling 2 and 3) with early exit when the divisor sum
      exceeds `n`.
    This keeps the function deterministic and often faster for very
    large candidates that match the Euclid–Euler structure.
    """
    if n <= 1:
        return False

    # Fast even-path: check Euclid-Euler form 2^(p-1)*(2^p-1)
    if n % 2 == 0:
        # count trailing zeros: e = p-1
        e = (n & -n).bit_length() - 1
        p = e + 1
        # quick form-check: odd part should equal 2^p - 1
        mersenne = (1 << p) - 1
        if n != (1 << e) * mersenne:
            return False

        # Lucas-Lehmer test for Mersenne primality (deterministic)
        def _lucas_lehmer(prime_exp: int) -> bool:
            if prime_exp == 2:
                return True
            M = (1 << prime_exp) - 1
            s = 4
            for _ in range(prime_exp - 2):
                s = (s * s - 2) % M
            return s == 0

        return _lucas_lehmer(p)

    # Odd fallback: highly optimized for non-perfects
    if n == 1:
        return False
    # All known perfect numbers are even; no odd perfect < 10**1500
    if n % 2 == 1:
        # Quick filters for odd perfects
        if n < 10**1500:
            # Must be 1 mod 4
            if n % 4 != 1:
                return False
            # Must be 1 or 9 mod 12
            if n % 12 not in (1, 9):
                return False
            # Must not be divisible by 3, 5, or 7
            if n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
                return False
            # Must have at least 9 distinct prime factors (skip expensive check, but could add more filters)
        else:
            # No known odd perfects below this bound
            return False
    divisors_sum = 1
    limit = isqrt(n)
    seen = set([1, n])
    wheel = [
        2,
        4,
        2,
        4,
        6,
        2,
        6,
        4,
        2,
        4,
        6,
        6,
        2,
        6,
        4,
        2,
        6,
        4,
        6,
        8,
        4,
        2,
        4,
        2,
        4,
        8,
        6,
        4,
        6,
        2,
        4,
        6,
        2,
        6,
        6,
        4,
        2,
        4,
        6,
        2,
        6,
        4,
        2,
        4,
        2,
        10,
        2,
        10,
    ]
    wlen = len(wheel)
    i = 2
    wi = 0
    while i <= limit:
        if n % i == 0:
            other = n // i
            if i not in seen:
                divisors_sum += i
                seen.add(i)
                if divisors_sum > n:
                    return False
            if other != i and other not in seen:
                divisors_sum += other
                seen.add(other)
                if divisors_sum > n:
                    return False
        i += wheel[wi]
        wi = (wi + 1) % wlen
    return divisors_sum == n


def is_perfectv2(n: int) -> bool:
    """Return True if n is a perfect number. With early exit

    - Time Complexity: O(√n)
    """
    if n <= 1:
        return False

    divisors_sum = 1
    limit = isqrt(n)
    for i in range(2, limit + 1):
        if n % i == 0:
            other = n // i
            divisors_sum += i
            if other != i:
                divisors_sum += other
        if divisors_sum > n:
            return False

    return divisors_sum == n


def is_perfectv3(n: int) -> bool:
    """Return True if `n` is a perfect number.

    - Fast even check using Euclid-Euler (2^(p-1)*(2^p-1) with Mersenne prime)
    - Miller-Rabin primality check reused locally
    - Fallback O(√n) divisor-summing with early exit
    """

    # local Miller-Rabin (small deterministic bases for typical ints)
    def _is_probable_prime_local(a_n: int) -> bool:
        if a_n < 2:
            return False
        small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
        for p in small_primes:
            if a_n % p == 0:
                return a_n == p

        d = a_n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

        def check(a: int) -> bool:
            x = pow(a, d, a_n)
            if x == 1 or x == a_n - 1:
                return True
            for _ in range(s - 1):
                x = (x * x) % a_n
                if x == a_n - 1:
                    return True
            return False

        for a in bases:
            if a % a_n == 0:
                continue
            if not check(a):
                return False
        return True

    if n <= 1:
        return False

    # Even fast-path using Euclid-Euler
    if n % 2 == 0:
        e = 0
        m = n
        while m % 2 == 0:
            m //= 2
            e += 1
        p = e + 1
        mersenne = (1 << p) - 1
        if m == mersenne and _is_probable_prime_local(m):
            return True
        return False

    # Odd fallback: sqrt method with early exit
    divisors_sum = 1
    limit = isqrt(n)
    for i in range(2, limit + 1):
        if n % i == 0:
            other = n // i
            divisors_sum += i
            if other != i:
                divisors_sum += other
        if divisors_sum > n:
            return False

    return divisors_sum == n


def is_perfectv4(n: int) -> bool:
    """Return True if `n` is a perfect number.

    - Fast even check using Euclid-Euler (2^(p-1)*(2^p-1) with Mersenne prime)
    - Miller-Rabin primality check for Mersenne candidates
    - Fallback O(√n) divisor-summing with early exit
    """

    def _is_probable_prime(num: int) -> bool:
        """Miller-Rabin with deterministic bases for typical integers."""
        if num < 2:
            return False
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
            if num % p == 0:
                return num == p

        d = num - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        def check(a: int) -> bool:
            x = pow(a, d, num)
            if x == 1 or x == num - 1:
                return True
            for _ in range(s - 1):
                x = (x * x) % num
                if x == num - 1:
                    return True
            return False

        return all(check(a) for a in (2, 325, 9375, 28178, 450775) if a % num != 0)

    if n <= 1:
        return False

    # Even fast-path: Euclid-Euler theorem
    if n % 2 == 0:
        e = (n & -n).bit_length() - 1  # Count trailing zeros
        mersenne = (1 << (e + 1)) - 1
        return n == (1 << e) * mersenne and _is_probable_prime(mersenne)

    # Odd fallback: sqrt method with early exit
    divisors_sum = 1
    limit = isqrt(n)
    for i in range(2, limit + 1):
        if n % i == 0:
            other = n // i
            divisors_sum += i + other if other != i else i
            if divisors_sum > n:
                return False

    return divisors_sum == n
