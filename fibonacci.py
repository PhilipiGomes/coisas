from functools import lru_cache


def fibv1(n):
    if n == 0:
        return 1
    return fibv1(n - 1) + fibv1(n - 2)


@lru_cache
def fibv2(n):
    if n == 0:
        return 1
    return fibv2(n - 1) + fibv2(n - 2)
