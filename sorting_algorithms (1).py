# sorting_algorithms.py
# Analysis of Algorithms - Sorting Assignment
# Name: Muhammad Hammad Ud Din   SAP: 65227
#
# In this file I have written 4 sorting algorithms by myself (no sort() used).
# All functions take the same parameters:
#   data       - the list we want to sort
#   key        - (optional) function to choose what to compare, like key=lambda s: s["marks"]
#   descending - True for big to small, False for small to big
#   stats      - (optional) SortStats object to count comparisons and swaps
# Each function makes a copy of the list so the original list does not change.


class SortStats:
    # used to count comparisons and swaps
    # (for merge sort I count writes instead of swaps)

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def reset(self):
        self.comparisons = 0
        self.swaps = 0


def _make_before(key, descending, stats):
    # this returns a function before(a, b)
    # it tells if a should come before b or not
    # I made this so all 4 sorts compare in the same way and count comparisons
    get = key if key is not None else (lambda x: x)

    def before(a, b):
        if stats is not None:
            stats.comparisons += 1
        if descending:
            return get(a) > get(b)
        return get(a) < get(b)

    return before


# 1. Selection Sort
# Time: O(n^2) in all cases
# Space: O(1) because it sorts in the same list
def selection_sort(data, key=None, descending=False, stats=None):
    arr = list(data)   # copy of the list
    before = _make_before(key, descending, stats)
    n = len(arr)

    for i in range(n - 1):
        best = i   # suppose first unsorted element is the smallest
        # find the actual smallest in remaining list
        for j in range(i + 1, n):
            if before(arr[j], arr[best]):
                best = j
        # swap only if smallest is not already at i
        if best != i:
            arr[i], arr[best] = arr[best], arr[i]
            if stats is not None:
                stats.swaps += 1
    return arr


# 2. Bubble Sort (stops early if no swap)
# Time: best case O(n) when already sorted, worst and average O(n^2)
# Space: O(1)
def bubble_sort(data, key=None, descending=False, stats=None):
    arr = list(data)
    before = _make_before(key, descending, stats)
    n = len(arr)

    for i in range(n - 1):
        swapped = False
        # last elements are already sorted after each pass so loop gets smaller
        for j in range(n - 1 - i):
            # swap if next element should come first
            if before(arr[j + 1], arr[j]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                if stats is not None:
                    stats.swaps += 1
        # if no swap happened list is sorted so break
        if not swapped:
            break
    return arr


# 3. Quick Sort
# Time: average O(n log n), worst O(n^2)
# Space: O(log n) for recursion because I call recursion on the smaller part first
#
# pivot="middle" is default, it takes the middle element so sorted and reverse
# sorted lists do not go to worst case.
# pivot="last" is the normal book method (Lomuto), I kept it to show worst case.
def quick_sort(data, key=None, descending=False, stats=None, pivot="middle"):
    arr = list(data)
    before = _make_before(key, descending, stats)

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]
        if stats is not None:
            stats.swaps += 1

    def partition(low, high):
        # if middle pivot, move it to the end first, then same partition works for both
        if pivot == "middle":
            mid = (low + high) // 2
            if mid != high:
                swap(mid, high)
        p = arr[high]
        boundary = low   # elements before boundary are smaller than pivot
        for j in range(low, high):
            if before(arr[j], p):
                if j != boundary:
                    swap(j, boundary)
                boundary += 1
        if boundary != high:
            swap(boundary, high)   # put pivot at its correct place
        return boundary

    def sort_range(low, high):
        # recursion on smaller side, loop on bigger side
        # so the recursion stack does not become too big
        while low < high:
            p = partition(low, high)
            if p - low < high - p:
                sort_range(low, p - 1)
                low = p + 1
            else:
                sort_range(p + 1, high)
                high = p - 1

    sort_range(0, len(arr) - 1)
    return arr


# 4. Merge Sort
# Time: O(n log n) in all cases
# Space: O(n) extra for the merged lists
# It is stable, so if two students have same marks their order stays same.
def merge_sort(data, key=None, descending=False, stats=None):
    before = _make_before(key, descending, stats)

    def merge(left, right):
        merged = []
        i = j = 0
        # take the smaller element from left or right
        # right is taken only if it is strictly smaller, this keeps it stable
        while i < len(left) and j < len(right):
            if before(right[j], left[i]):
                merged.append(right[j]); j += 1
            else:
                merged.append(left[i]); i += 1
            if stats is not None:
                stats.swaps += 1   # counting this as a write
        # add remaining elements
        for item in left[i:] + right[j:]:
            merged.append(item)
            if stats is not None:
                stats.swaps += 1
        return merged

    def split(arr):
        if len(arr) <= 1:
            return list(arr)
        mid = len(arr) // 2
        return merge(split(arr[:mid]), split(arr[mid:]))

    return split(list(data))


# dictionary of all algorithms, used in benchmark.py
ALGORITHMS = {
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}
