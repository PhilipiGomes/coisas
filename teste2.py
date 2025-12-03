import perfect_nums
from time import perf_counter
import sys
sys.set_int_max_str_digits(7000)
# trunk-ignore(ruff/E402)
from numeros_perfeitos import nums


n = nums[-1]
start = perf_counter()
res = perfect_nums.is_perfectv6(n)
end = perf_counter()

print(n, res, round(end-start, 10))