import math
import time


def is_primev1(n: int) -> bool:
    """
    Basic primality test counting the number of divisors.
    - Time Complexity (worst-case): O(n)
    - Space Complexity: O(1)
    """
    num = 0
    for i in range(2, n + 1):
        if n % i == 0:
            num += 1
    if num > 2:
        return False
    return True


def is_primev2(n: int) -> bool:
    """
    Simple optimization by returning early when a divisor is found.
    - Time Complexity (worst-case): O(n)
    - Space Complexity: O(1)
    """
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def is_primev3(n: int) -> bool:
    """
    Optimization by checking only odd numbers after 2.
    - Time Complexity (worst-case): O(n)   (more precisely O(n/2) iterations)
    - Space Complexity: O(1)
    """
    if n % 2 == 0 and n != 2:
        return False
    for i in range(3, n, 2):
        if n % i == 0:
            return False
    return True


def is_primev4(n: int) -> bool:
    """
    Optimization by checking divisors only up to the square root of n.
    - Time Complexity (worst-case): O(√n)
    - Space Complexity: O(1)
    """
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_primev5(n: int) -> bool:
    """
    Same as is_prime_v1, but counting divisors only up to the square root of n.
    - Time Complexity (worst-case): O(√n)
    - Space Complexity: O(√n) for the divisors list (in the divisors helper)
    """

    def divisors(x: int) -> list[int]:
        """
        Finding the divisors of x up to its square root.
        - Time Complexity: O(√x)
        - Space Complexity: O(√x) in the worst case (list of divisors)
        """
        divs = [1, x]
        for i in range(2, int(math.sqrt(x))):
            if x % i == 0:
                divs.append(i)
                divs.append(x // i)
        return divs

    num_divs = len(divisors(n))
    if num_divs > 2:
        return False
    return True


def is_primev6(n: int) -> bool:
    """
    Optimization by checking only odd numbers after 2, up to the square root of n.
    - Time Complexity (worst-case): O(√n)   (more precisely ~ O(√n / 2) iterations)
    - Space Complexity: O(1)
    """
    if n % 2 == 0 and n != 2:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_primev7(n: int) -> bool:
    """
    Optimization using 6k ± 1 rule, and returning early for multiples of 2 and 3.
    - Time Complexity (worst-case): O(√n)   (more precisely ~ O(√n / 6) iterations)
    - Space Complexity: O(1)
    """
    if n == 2 or n == 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i < int(math.sqrt(n)) + 1:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def main(n: int, num_times: int):
    funcs = {
        "is_primev1": is_primev1,
        "is_primev2": is_primev2,
        "is_primev3": is_primev3,
        "is_primev4": is_primev4,
        "is_primev5": is_primev5,
        "is_primev6": is_primev6,
        "is_primev7": is_primev7,
    }

    times = {}

    for name, func in funcs.items():
        print(f"Testing function {name}")

        mean = 0

        for _ in range(num_times):
            start = time.perf_counter()
            func(n)
            end = time.perf_counter()
            mean += end - start

        mean /= num_times

        times[name] = round(mean, 10)

    # sort by time
    times_sorted = dict(sorted(times.items(), key=lambda x: x[1]))

    # get name of fastest function
    fastest_name = next(iter(times_sorted))

    # execute the fastest function to see the primality of the number
    prime = funcs[fastest_name](n)

    print()
    print(f"Elapsed time by function to verify the primality of the number {n}")
    print()
    print("Ranking\tFunction name\tElapsed Time")

    for i, (name, elap) in enumerate(times_sorted.items(), start=1):
        print(f"{i}\t{name}\t{elap}")

    print()
    print(f"The number {n} is {'prime' if prime else 'composite'}.")


main(2**20 - 1, 2000)
