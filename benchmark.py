import json
import platform
import random
import time
import tracemalloc

from sorting_algorithms import ALGORITHMS, SortStats, quick_sort

RUNS = 3
REPEATS = 3000

CASES = {
    "Size 5 - Sorted":           list(range(1, 6)),
    "Size 5 - Reverse Sorted":   list(range(5, 0, -1)),
    "Size 100 - Sorted":         list(range(1, 101)),
    "Size 100 - Reverse Sorted": list(range(100, 0, -1)),
}


def time_one_run(sort_fn, data):
    start = time.perf_counter()
    for _ in range(REPEATS):
        sort_fn(data)
    end = time.perf_counter()
    return (end - start) / REPEATS * 1_000_000


def peak_memory(sort_fn, data):
    tracemalloc.start()
    sort_fn(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def count_operations(sort_fn, data):
    stats = SortStats()
    result = sort_fn(data, stats=stats)
    assert result == sorted(data), "sort produced a wrong result"
    return stats.comparisons, stats.swaps


def quick_last_pivot(data, **kw):
    return quick_sort(data, pivot="last", **kw)


def main():
    algos = dict(ALGORITHMS)
    algos["Quick Sort (last pivot)"] = quick_last_pivot

    for fn in algos.values():
        for data in CASES.values():
            for _ in range(200):
                fn(data)

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
