import time
import random
import matplotlib.pyplot as plt


def measure_time(sort_function, arr):
    start_time = time.time()
    sort_function(arr)
    end_time = time.time()
    return end_time - start_time


def insertion_sort(array_, left=0, right=None):
    # Got this implementation of insertion sort from this link:
    # https://www.geeksforgeeks.org/python-program-for-insertion-sort/
    if right is None:
        right = len(array_) - 1

    for i in range(left + 1, right + 1):
        key = array_[i]
        j = i - 1
        while j >= left and key < array_[j]:
            array_[j + 1] = array_[j]
            j -= 1
        array_[j + 1] = key


def merge_sort(array_):
    # Got this implementation of merge sort from this link:
    # https://how.dev/answers/merge-sort-in-python
    if len(array_) > 1:
        mid = len(array_) // 2
        left_half = array_[:mid]
        right_half = array_[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = 0
        j = 0
        k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                array_[k] = left_half[i]
                i += 1
            else:
                array_[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            array_[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            array_[k] = right_half[j]
            j += 1
            k += 1

def tim_sort(array_, k):
    # I used this link to implement tim sort:
    # https://www.geeksforgeeks.org/tim-sort-in-python/

    n = len(array_)

    for i in range(0, n, k):
        insertion_sort(array_, i, min(i + k - 1, (n - 1)))

    size = k
    while size < n:
        for start in range(0, n, size * 2):
            midpoint = start + size
            end = min((start + size * 2 - 1), (n - 1))

            left = array_[start:midpoint]
            right = array_[midpoint:end + 1]

            merged = []
            i = j = 0

            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1

            merged.extend(left[i:])
            merged.extend(right[j:])

            array_[start:start + len(merged)] = merged

        size *= 2

    return array_


k_values = [8, 16, 32, 64, 128, 256, 1024]
n_values = [100, 500, 1000]
results = {"Insertion Sort": {}, "Merge Sort": {}, "Tim Sort": {}}

for n in n_values:
    test_list = []
    for _ in range(n):
        test_list.append(random.randint(1, 10000))

    insertion_copy = test_list.copy()
    merge_copy = test_list.copy()

    insertion_time = measure_time(lambda array_: insertion_sort(array_), insertion_copy)
    results["Insertion Sort"][n] = insertion_time

    merge_time = measure_time(lambda array_: merge_sort(array_), merge_copy)
    results["Merge Sort"][n] = merge_time

    tim_times = []
    for k in k_values:
        tim_copy = test_list.copy()
        tim_time = measure_time(lambda array_: tim_sort(array_, k), tim_copy)
        tim_times.append(tim_time)

    results["Tim Sort"][n] = tim_times

plt.figure(figsize=(10, 6))

for sort_type in ["Insertion Sort", "Merge Sort"]:
    times = []
    for n in n_values:
        times.append(results[sort_type][n])
    plt.plot(n_values, times, marker='o', label=sort_type)

for i, k in enumerate(k_values):
    tim_times = []
    for n in n_values:
        tim_times.append(results["Tim Sort"][n][i])
    plt.plot(n_values, tim_times, marker='s', linestyle='dashed', label=f'Tim Sort (k={k})')

plt.xlabel('Number of Elements (n)')
plt.ylabel('Time (seconds)')
plt.title('Insertion Sort, Merge Sort, and Tim Sort Comparison')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.savefig("tim_sort.png")
