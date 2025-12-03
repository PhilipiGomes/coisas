import time

import matplotlib.pyplot as plt

import perfect_nums


def time_function(fn, n, repeats=1):
    """Measure average execution time of fn(n) over `repeats` runs using perf_counter."""
    start = time.perf_counter()
    for _ in range(repeats):
        fn(n)
    end = time.perf_counter()
    return (end - start) / repeats


if __name__ == "__main__":
    # User-configurable interval and sampling
    start_n = 2  # <-- change start value here
    end_n = 1000  # <-- change end value here
    step = 1  # step between n values
    repeats = 1000  # increase if function is very fast (e.g., 100 or 1000)
    # Function to profile
    func = perfect_nums.is_perfectv5

    ns = list(range(start_n, end_n + 1, step))
    times = []
    for n in ns:
        t = time_function(func, n, repeats=repeats)
        times.append(t)

    plt.plot(ns, times, linestyle="None", marker="o", label=f"{func.__name__}")
    # Plot the line y = x for comparison
    scale = max(times) / max(ns)
    plt.plot(ns, [scale * x for x in ns], "--", color="red", label="y = x (scaled)")
    plt.xlabel("n")
    plt.ylabel("time (s)")
    plt.title(f"Execution time of {func.__name__} (repeats={repeats})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
