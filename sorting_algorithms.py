class SortStats:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def reset(self):
        self.comparisons = 0
        self.swaps = 0


def _make_before(key, descending, stats):
    get = key if key is not None else (lambda x: x)

    def before(a, b):
        if stats is not None:
            stats.comparisons += 1
        if descending:
            return get(a) > get(b)
        return get(a) < get(b)

    return before


def selection_sort(data, key=None, descending=False, stats=None):
    arr = list(data)
    before = _make_before(key, descending, stats)
    n = len(arr)

    for i in range(n - 1):
        best = i
        for j in range(i + 1, n):
            if before(arr[j], arr[best]):
                best = j
        if best != i:
            arr[i], arr[best] = arr[best], arr[i]
            if stats is not None:
                stats.swaps += 1
    return arr


def bubble_sort(data, key=None, descending=False, stats=None):
    arr = list(data)
    before = _make_before(key, descending, stats)
    n = len(arr)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if before(arr[j + 1], arr[j]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                if stats is not None:
                    stats.swaps += 1
        if not swapped:
            break
    return arr


def quick_sort(data, key=None, descending=False, stats=None, pivot="middle"):
    arr = list(data)
    before = _make_before(key, descending, stats)

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]
        if stats is not None:
            stats.swaps += 1

    def partition(low, high):
        if pivot == "middle":
            mid = (low + high) // 2
            if mid != high:
                swap(mid, high)
        p = arr[high]
        boundary = low
        for j in range(low, high):
            if before(arr[j], p):
                if j != boundary:
                    swap(j, boundary)
                boundary += 1
        if boundary != high:
            swap(boundary, high)
        return boundary

    def sort_range(low, high):
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


def merge_sort(data, key=None, descending=False, stats=None):
    before = _make_before(key, descending, stats)

    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if before(right[j], left[i]):
                merged.append(right[j]); j += 1
            else:
                merged.append(left[i]); i += 1
            if stats is not None:
                stats.swaps += 1
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


ALGORITHMS = {
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}
