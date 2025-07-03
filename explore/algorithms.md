# Essential Algorithms for High-Level Interviews

This guide covers key algorithms, including their titles, explanations, time and space complexities, approaches, detailed steps, and code examples. Each section is formatted for clarity and quick reference.

---

## 1. Sorting Algorithms

### 1.1 Bubble Sort

**Explanation:**  
Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The process repeats until the list is sorted.

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

**Approach:**  
Iterate through the array, swapping adjacent elements if out of order. Repeat until no swaps are needed.

**Detailed Steps:**
1. Start at the beginning of the array.
2. Compare each pair of adjacent elements.
3. Swap if the left element is greater than the right.
4. Repeat for all elements, reducing the range each time.
5. Stop if no swaps occurred in a pass.

**Code Example (Python):**
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

---

### 1.2 Selection Sort

**Explanation:**  
Finds the minimum element from the unsorted part and puts it at the beginning. Repeats for all positions.

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

**Approach:**  
For each position, find the minimum in the unsorted part and swap.

**Detailed Steps:**
1. Start from the first element.
2. Find the minimum in the unsorted part.
3. Swap it with the current element.
4. Move to the next position and repeat.

**Code Example (Python):**
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

---

### 1.3 Insertion Sort

**Explanation:**  
Builds the sorted array one element at a time by inserting each element into its correct position.

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

**Approach:**  
Iterate, inserting each element into its correct position in the sorted part.

**Detailed Steps:**
1. Start from the second element.
2. Compare with elements before it.
3. Shift larger elements right.
4. Insert the element at the correct position.

**Code Example (Python):**
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

---

### 1.4 Merge Sort

**Explanation:**  
A divide-and-conquer algorithm that splits the array, sorts each half, and merges them.

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

**Approach:**  
Recursively split the array, sort, and merge.

**Detailed Steps:**
1. Divide the array into halves.
2. Recursively sort each half.
3. Merge the sorted halves.

**Code Example (Python):**
```python
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr
```

---

### 1.5 Quick Sort

**Explanation:**  
Selects a pivot, partitions the array, and recursively sorts the partitions.

**Time Complexity:** O(n log n) average, O(n²) worst  
**Space Complexity:** O(log n)

**Approach:**  
Choose a pivot, partition, and recursively sort subarrays.

**Detailed Steps:**
1. Pick a pivot.
2. Partition elements into less than, equal to, and greater than pivot.
3. Recursively sort partitions.

**Code Example (Python):**
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

---

## 2. Searching Algorithms

### 2.1 Linear Search

**Explanation:**  
Checks each element until the target is found.

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

**Approach:**  
Iterate and compare each element to the target.

**Detailed Steps:**
1. Start from the first element.
2. Compare with the target.
3. Return index if found, else continue.

**Code Example (Python):**
```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

---

### 2.2 Binary Search

**Explanation:**  
Efficiently searches a sorted array by repeatedly dividing the search interval in half.

**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

**Approach:**  
Compare target to the middle element, halve the search space.

**Detailed Steps:**
1. Set low and high pointers.
2. Find the middle element.
3. If target equals middle, return index.
4. If target < middle, search left half.
5. If target > middle, search right half.

**Code Example (Python):**
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

---

### 2.3 Jump Search

**Explanation:**  
Jumps ahead by fixed steps in a sorted array, then does linear search in the block.

**Time Complexity:** O(√n)  
**Space Complexity:** O(1)

**Approach:**  
Jump in steps, then search linearly in the identified block.

**Detailed Steps:**
1. Calculate step size (√n).
2. Jump ahead by step size until target is exceeded.
3. Do linear search in the last block.

**Code Example (Python):**
```python
import math

def jump_search(arr, target):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return -1
```

---

## 3. Graph Algorithms

### 3.1 Depth-First Search (DFS)

**Explanation:**  
Explores as far as possible along each branch before backtracking.

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

**Approach:**  
Use recursion or a stack to traverse nodes deeply.

**Detailed Steps:**
1. Start at a node.
2. Visit and mark as visited.
3. Recursively visit all unvisited neighbors.

**Code Example (Python):**
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

---

### 3.2 Breadth-First Search (BFS)

**Explanation:**  
Explores all neighbors at the current depth before moving to the next level.

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

**Approach:**  
Use a queue to traverse nodes level by level.

**Detailed Steps:**
1. Start at a node, enqueue it.
2. Dequeue a node, visit and mark as visited.
3. Enqueue all unvisited neighbors.
4. Repeat until queue is empty.

**Code Example (Python):**
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited
```

---

## 4. Dynamic Programming

### 4.1 Fibonacci Sequence (DP)

**Explanation:**  
Computes Fibonacci numbers efficiently by storing previous results.

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Approach:**  
Use an array to store computed values.

**Detailed Steps:**
1. Initialize base cases.
2. Iteratively compute each Fibonacci number using previous two.

**Code Example (Python):**
```python
def fibonacci(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

---

## 5. Greedy Algorithms

### 5.1 Activity Selection Problem

**Explanation:**  
Selects the maximum number of non-overlapping activities.

**Time Complexity:** O(n log n)  
**Space Complexity:** O(1)

**Approach:**  
Sort activities by end time, select compatible ones.

**Detailed Steps:**
1. Pair activities with start and end times.
2. Sort by end time.
3. Select the first activity.
4. For each next activity, if its start time ≥ last selected's end time, select it.

**Code Example (Python):**
```python
def activity_selection(start, end):
    activities = sorted(zip(start, end), key=lambda x: x[1])
    selected = []
    last_end = -1
    for s, e in activities:
        if s >= last_end:
            selected.append((s, e))
            last_end = e
    return selected
```

---

## Formatting Guidelines

- **Title:** Algorithm name and category.
- **Explanation:** What the algorithm does and when to use it.
- **Time/Space Complexity:** Big-O notation.
- **Approach:** High-level strategy.
- **Detailed Steps:** Step-by-step breakdown.
- **Code Example:** Python implementation.

---

This structure ensures clarity and completeness for interview preparation. Expand with more algorithms as needed!
