# Sorting Algorithms Analysis

Assignment 03 - Analysis of Algorithms
Muhammad Hammad Ud Din (SAP 65227)
Submitted to: Sir Usman Sharif

In this assignment I wrote 4 sorting algorithms in Python without using the built-in sort():

- Selection Sort
- Bubble Sort (stops early if no swap)
- Quick Sort (middle pivot)
- Merge Sort

Each one is tested on 4 arrays (size 5 and size 100, sorted and reverse sorted), so 16 experiments in total.
For every experiment I measured the time (average of 3 runs), the peak memory, and the number of comparisons and swaps.

## Files

| File | What it has |
|------|-------------|
| `sorting_algorithms.py` | the 4 sorting algorithms |
| `benchmark.py` | runs all 16 experiments and prints the tables |
| `results.json` | the results I used in my report |

## How to run

You need Python 3. No extra library is needed.

```
python benchmark.py
```

It prints the results for each case and saves them in `results.json`.
Times will be a little different on every computer, but comparisons and swaps will be the same.

## Results (average time in microseconds)

| Algorithm | Size 5 Sorted | Size 5 Reverse | Size 100 Sorted | Size 100 Reverse |
|-----------|--------------:|---------------:|----------------:|-----------------:|
| Selection Sort | 1.63 | 1.72 | 419.26 | 404.07 |
| Bubble Sort | 0.85 | 1.97 | 8.71 | 671.21 |
| Quick Sort | 4.46 | 3.95 | 69.15 | 79.96 |
| Merge Sort | 4.27 | 4.55 | 100.83 | 112.04 |

Full analysis is in the report PDF.
