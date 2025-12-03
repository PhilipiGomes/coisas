import sys
from time import perf_counter

sys.set_int_max_str_digits(8000)
# trunk-ignore(ruff/E402)
from tqdm import tqdm

# trunk-ignore(ruff/E402)
from perfect_nums import is_perfectv6

min_n = 10**6000
max_n = 10**6010

if min_n > max_n:
    raise Exception("The minimum can not be bigger then the maximum")

perfect = []


def big_range(start, stop):
    n = start
    while n <= stop:
        yield n
        n += 1


for i in tqdm(
    big_range(min_n, max_n),
    "Finding perfect numbers",
    unit="num",
):
    start = perf_counter()
    res = is_perfectv6(i)
    end = perf_counter()
    if res:
        perfect.append(i)
        tqdm.write(f"Found perfect number: {i}")


if perfect:
    # print a summary line at the end
    print("Perfect numbers found:", end=" ")
    print(*perfect, sep=", ")
