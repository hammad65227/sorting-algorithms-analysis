# benchmark.py
# Analysis of Algorithms - Sorting Assignment
# Name: Muhammad Hammad Ud Din   SAP: 65227
#
# This file runs all 16 experiments (4 algorithms x 4 cases) and finds:
#   1. Time   - average of 3 runs using time.perf_counter()
#   2. Space  - peak memory using tracemalloc
#   3. Number of comparisons and swaps
#
# Note: sorting 5 numbers is very fast (around 1 microsecond) so the timer
# can not measure it properly. So in each run I sort the same list REPEATS
# times and then divide by REPEATS. This still gives time for one sort.
#
# To run:  python benchmark.py   (results also saved in results.json)

import json
import platform
import random
import time
import tracemalloc

from sorting_algorithms import ALGORITHMS, SortStats, quick_sort

RUNS = 3          # 3 runs as asked in assignment
REPEATS = 3000    # number of sorts in one run

CASES = {
    "Size 5 - Sorted":           list(range(1, 6)),
    "Size 5 - Reverse Sorted":   list(range(5, 0, -1)),
    "Size 100 - Sorted":         list(range(1, 101)),
    "Size 100 - Reverse Sorted": list(range(100, 0, -1)),
}


def time_one_run(sort_fn, data):
    # start timer, sort REPEATS times, stop timer, return time of one sort in microseconds
    start = time.perf_counter()
    for _ in range(REPEATS):
        sort_fn(data)   # function copies data so input is same every time
    end = time.perf_counter()
    return (end - start) / REPEATS * 1_000_000


def peak_memory(sort_fn, data):
    # peak memory in bytes while sorting (copy of list is also included)
    tracemalloc.start()
    sort_fn(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def count_operations(sort_fn, data):
    stats = SortStats()
    result = sort_fn(data, stats=stats)
    assert result == sorted(data), "sort produced a wrong result"   # just checking the answer is correct
    return stats.comparisons, stats.swaps


def quick_last_pivot(data, **kw):
    # quick sort with last element as pivot (extra experiment)
    return quick_sort(data, pivot="last", **kw)


def main():
    algos = dict(ALGORITHMS)
    algos["Quick Sort (last pivot)"] = quick_last_pivot

    # warm up - run everything once before timing
    # so the first algorithm does not get extra time
    for fn in algos.values():
        for data in CASES.values():
            for _ in range(200):
                fn(data)

    # first do run 1 of all cases, then run 2, then run 3
    # order is shuffled every time so if computer slows down for a moment
    # it does not affect only one algorithm
    jobs = [(c, a) for c in CASES for a in algos]
    times = {job: [] for job in jobs}
    order = random.Random(7)
    for _ in range(RUNS):
        order.shuffle(jobs)
        for case_name, algo_name in jobs:
            times[(case_name, algo_name)].append(time_one_run(algos[algo_name], CASES[case_name]))

    results = {"machine": f"{platform.machine()} | Python {platform.python_version()} | {platform.system()}",
               "runs": RUNS, "repeats": REPEATS, "cases": {}, "quick_last_pivot": {}}

    for case_name, data in CASES.items():
        print(f"\n{case_name}")
        print(f"{'Algorithm':15s} {'Run1':>9s} {'Run2':>9s} {'Run3':>9s} {'Avg(us)':>9s}"
              f" {'Comps':>6s} {'Swaps':>6s} {'Peak B':>7s}")
        rows = []
        for algo_name, sort_fn in ALGORITHMS.items():
            runs = times[(case_name, algo_name)]
            avg = sum(runs) / RUNS
            comps, swaps = count_operations(sort_fn, data)
            mem = peak_memory(sort_fn, data)
            rows.append({"algorithm": algo_name, "runs_us": runs, "avg_us": avg,
                         "comparisons": comps, "swaps": swaps, "peak_bytes": mem})
            print(f"{algo_name:15s} {runs[0]:9.2f} {runs[1]:9.2f} {runs[2]:9.2f} {avg:9.2f}"
                  f" {comps:6d} {swaps:6d} {mem:7d}")
        results["cases"][case_name] = rows

        runs = times[(case_name, "Quick Sort (last pivot)")]
        comps, swaps = count_operations(quick_last_pivot, data)
        results["quick_last_pivot"][case_name] = {"avg_us": sum(runs) / RUNS,
                                                  "comparisons": comps, "swaps": swaps}

    print("\nExtra: Quick Sort with LAST-element pivot")
    for case_name, r in results["quick_last_pivot"].items():
        print(f"{case_name:26s} avg {r['avg_us']:8.2f} us  comps {r['comparisons']}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved results.json")


if __name__ == "__main__":
    main()
