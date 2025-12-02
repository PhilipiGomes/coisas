from typing import Tuple


def evaluate(n: int, s: int, m: int, d: int, h: int) -> int:
    return n * (s * m + d) * h + 1


def maximize(total:int) -> Tuple[Tuple[int, int, int, int, int], int]:
    max_value = -1
    best_params = (0, 0, 0, 0, 0)

    for n in range(1, total + 1):
        for s in range(1, total - n + 1):
            for m in range(1, total - (n * s) + 1):
                for d in range(1, total - (n * s * m) + 1):
                    h = total - (n * s * m * d)
                    if h < 1:
                        continue
                    current_value = evaluate(n, s, m, d, h)
                    print(f"Evaluating n={n}, s={s}, m={m}, d={d}, h={h}, value={current_value}")
                    if current_value > max_value:
                        max_value = current_value
                        best_params = (n, s, m, d, h)

    return best_params, max_value


if __name__ == "__main__":
    total = 100
    (n, s, m, d, h), max_value = maximize(total)
    print(f"Maximized parameters for total {total}: n={n}, s={s}, m={m}, d={d}, h={h}")
    print(f"Maximum value: {max_value}")