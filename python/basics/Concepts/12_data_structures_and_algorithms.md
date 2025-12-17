# Data Structures and Algorithms: Effective Python Best Practices

## 1. Sort by Complex Criteria Using the key Parameter

### Explanation
Python’s `sorted()` and list `.sort()` accept a `key` function that transforms each element to a value used for comparison. This is the **recommended way** to sort by:
- Multiple fields
- Derived/computed values
- Case-insensitive comparisons, etc.

### Use Cases
- Sorting objects (dicts, custom classes) by fields
- Sorting by multiple criteria (e.g., primary and secondary keys)
- Custom orderings without modifying the original data

### Examples

```python
users = [
    {"name": "Alice", "age": 30},
    {"name": "bob", "age": 25},
    {"name": "Charlie", "age": 20},
]

# ❌ BAD: Writing custom comparison logic manually (old-style, harder)
# In Python 3, cmp-style functions are not supported directly.

# ✅ GOOD: Sort by age
by_age = sorted(users, key=lambda u: u["age"])

# ✅ GOOD: Case-insensitive sort by name
by_name_ci = sorted(users, key=lambda u: u["name"].lower())

# ✅ GOOD: Sort by multiple criteria: age ascending, then name
by_age_then_name = sorted(
    users, key=lambda u: (u["age"], u["name"].lower())
)

print(by_age)
print(by_name_ci)
print(by_age_then_name)
```

Sorting custom objects:

```python
class User:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"User({self.name!r}, {self.score})"

users = [
    User("Alice", 90),
    User("Bob", 75),
    User("Charlie", 90),
]

# Sort by score descending, then name ascending
sorted_users = sorted(
    users,
    key=lambda u: (-u.score, u.name)
)
print(sorted_users)
```

### Tips
- Use tuples in `key` for multi-field sorting
- For descending sort, often easier to negate numeric fields (e.g., `-x`) or use `reverse=True` globally

---

## 2. Know the Difference Between sort and sorted

### Explanation
- `sorted(iterable, ...)` returns a **new list**, leaving the original iterable unchanged
- `.sort()` is a **list method** that sorts **in place** and returns `None`

### Use Cases
- Use `sorted()` when:
  - You need a new sorted list
  - You’re sorting non-list iterables (e.g., tuples, sets, generators)
- Use `.sort()` when:
  - You already have a list and want to mutate it in place

### Examples

```python
data = [3, 1, 4, 1, 5]

# sorted() – returns a new list, does not modify original
new_list = sorted(data)
print(data)      # [3, 1, 4, 1, 5]
print(new_list)  # [1, 1, 3, 4, 5]

# .sort() – modifies in place, returns None
data.sort()
print(data)      # [1, 1, 3, 4, 5]
```

Sorting other iterables:

```python
numbers = {3, 1, 4, 1, 5}
sorted_set = sorted(numbers)  # returns list [1, 3, 4, 5]

text = "python"
sorted_chars = sorted(text)   # ['h', 'n', 'o', 'p', 't', 'y']
```

### Guidelines
- Don’t write `data = data.sort()` – `.sort()` returns `None`
- Prefer `sorted()` for clarity unless you really need in-place modification

---

## 3. Consider Searching Sorted Sequences with bisect

### Explanation
The `bisect` module provides efficient binary search operations on **sorted lists**:
- `bisect_left` / `bisect_right` to find insertion positions
- `insort_left` / `insort_right` to insert while maintaining order

These operations run in **O(log n)** for searching (but insertions into lists are still O(n) due to shifting).

### Use Cases
- Maintaining a sorted list as you insert values
- Finding insertion points for thresholds (e.g., grade cutoffs)
- Implementing simple ordered indexes

### Examples

```python
import bisect

scores = [10, 20, 30, 40, 50]  # must be sorted

pos = bisect.bisect_left(scores, 35)
print(pos)  # 3 (scores[3] == 40, first >= 35)

pos = bisect.bisect_right(scores, 30)
print(pos)  # 3 (insertion after existing 30)

# Use insort to keep list sorted
bisect.insort(scores, 35)
print(scores)  # [10, 20, 30, 35, 40, 50]
```

Threshold example:

```python
import bisect

breakpoints = [60, 70, 80, 90]      # sorted
grades      = ["F", "D", "C", "B", "A"]

def grade(score):
    i = bisect.bisect(breakpoints, score)
    return grades[i]

print(grade(55))  # F
print(grade(65))  # D
print(grade(75))  # C
print(grade(85))  # B
print(grade(95))  # A
```

### Tips
- Use `bisect` when you need **fast repeated searches** in a sorted sequence
- For heavy insertion workloads, consider other structures (e.g., `bisect` + `deque`, or specialized libraries like `sortedcontainers`)

---

## 4. Prefer deque for Producer-Consumer Queues

### Explanation
`collections.deque` is a double-ended queue optimized for:
- **O(1)** appends and pops from **both ends**
- Efficient queue and stack behavior

Lists are O(1) for `append`/`pop` at the end, but O(n) for operations at the beginning (`pop(0)`, `insert(0, ...)`).

### Use Cases
- FIFO queues (`append` + `popleft`)
- LIFO stacks (`append` + `pop`)
- Sliding window operations

### Examples

```python
from collections import deque

q = deque()

# Producer
q.append("task1")
q.append("task2")

# Consumer (FIFO)
task = q.popleft()
print(task)  # "task1"
\n# Sliding window example
window = deque(maxlen=3)

for x in [1, 2, 3, 4, 5]:
    window.append(x)
    print(list(window))
    # Output:
    # [1]
    # [1, 2]
    # [1, 2, 3]
    # [2, 3, 4]
    # [3, 4, 5]
```

### Guidelines
- Use `deque` instead of `list` when you frequently:
  - Push/pop from the **left**
  - Need a fixed-length FIFO/LRU buffer

---

## 5. Know How to Use heapq for Priority Queues

### Explanation
The `heapq` module implements a **min-heap** using a list. A heap is good for:
- Getting/removing the **smallest** item in O(log n)
- Maintaining a priority queue (e.g., tasks with priorities)

### Use Cases
- Scheduling tasks by priority
- Implementing algorithms (Dijkstra, A* search, etc.)
- Keeping top-N smallest or largest elements

### Examples

```python
import heapq

numbers = [5, 3, 8, 1, 2]
heap = []

for n in numbers:
    heapq.heappush(heap, n)

print(heapq.heappop(heap))  # 1
print(heapq.heappop(heap))  # 2
print(heapq.heappop(heap))  # 3
```

Priority queue with (priority, item) tuples:

```python
import heapq

tasks = []

heapq.heappush(tasks, (2, "low priority"))
heapq.heappush(tasks, (1, "high priority"))
heapq.heappush(tasks, (3, "very low priority"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(priority, task)
```

Top-N elements:

```python
import heapq

nums = [5, 1, 8, 3, 7, 2]
print(heapq.nsmallest(3, nums))  # [1, 2, 3]
print(heapq.nlargest(2, nums))   # [8, 7]
```

### Tips
- Store `(priority, counter, item)` if you need a **stable** priority queue
- Remember: `heapq` is a **min-heap**; for max-heap behavior, store negative priorities or use `nlargest`

---

## 6. Use datetime Instead of time for Local Clocks

### Explanation
The `time` module works with POSIX timestamps (seconds since epoch) and low-level time functions. The `datetime` module provides:
- Time zone–aware `datetime` objects
- Clear separation of **date**, **time**, and **timedelta**
- Easier manipulation and formatting

### Use Cases
- Dealing with human-readable times and dates
- Time zone conversions
- Adding/subtracting days, hours, minutes

### Examples

```python
from datetime import datetime, timedelta, timezone

now_utc = datetime.now(timezone.utc)
print(now_utc)

# Convert to local time (example: naive local)
now_local = now_utc.astimezone()  # system local tz
print(now_local)

# Add 7 days
one_week_later = now_local + timedelta(days=7)
print(one_week_later)

# Formatting
print(now_local.strftime("%Y-%m-%d %H:%M:%S %Z"))

# Parsing
dt = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
print(dt)
```

Comparing time durations:

```python
start = datetime.now()
do_work()
end = datetime.now()

duration = end - start  # timedelta
print(duration.total_seconds(), "seconds")
```

### Guidelines
- Prefer `datetime` over raw `time.time()` for application-level time handling
- Use `timezone-aware` datetimes (`tzinfo`) for anything that crosses time zones

---

## 7. Use decimal When Precision Is Paramount

### Explanation
Binary floating-point (`float`) cannot represent all decimal fractions exactly. This can cause surprising rounding errors, especially in **financial** or high-precision domains. The `decimal` module provides:
- Decimal-based arithmetic
- Configurable precision and rounding

### Use Cases
- Money calculations (currencies)
- Situations that require exact decimal representation

### Examples

```python
from decimal import Decimal, getcontext

print(0.1 + 0.2)           # 0.30000000000000004

a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)               # 0.3 (exact)

# Set precision
getcontext().prec = 6

x = Decimal("1") / Decimal("7")
print(x)                   # 0.142857
```

Money example:

```python
price  = Decimal("19.99")
tax    = Decimal("0.075")  # 7.5%
total  = price + price * tax
print(total)               # precise decimal result
```

### Guidelines
- Use `Decimal("...")` with **string** input, not `Decimal(0.1)`
- Use floats for scientific/engineering where small rounding is acceptable
- Use `decimal` for finance/business logic

---

## 8. Make pickle Serialization Maintainable with copyreg

### Explanation
`pickle` serializes Python objects, but if you change class definitions (e.g., rename, change constructor) later, old pickles may break.  
`copyreg` lets you **register custom pickling functions** for your types to control how they’re serialized/deserialized in a forward-compatible way.

### Use Cases
- Persisting objects to disk between versions of your code
- Custom classes that need stable, explicit serialization format

### Examples

```python
import copyreg
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def pickle_point(point):
    # Return (callable, args) to reconstruct the object
    return Point, (point.x, point.y)

copyreg.pickle(Point, pickle_point)

p = Point(2, 3)
data = pickle.dumps(p)
restored = pickle.loads(data)
print(restored.x, restored.y)
```

This way, if you later change the internal representation of `Point`, you can update `pickle_point` (and/or the reconstruction callable) to keep existing pickles loadable.

### Guidelines
- Prefer simple, explicit state for pickling (e.g., tuples, dicts)
- Use `copyreg` for custom classes where you care about long-term compatibility
- Remember that `pickle` is **Python-specific** and not safe for untrusted input

---

## Summary

These eight principles help you use Python’s built-in data structures and algorithms effectively:

1. **key parameter for sorting** – Express complex sort criteria cleanly  
2. **sort vs sorted** – Know when to use in-place vs new list  
3. **bisect** – Efficient binary search on sorted sequences  
4. **deque** – Fast queues and sliding windows  
5. **heapq** – Priority queues and top-N operations  
6. **datetime** – Safer, clearer time handling than raw timestamps  
7. **decimal** – Exact decimal math when precision matters  
8. **copyreg + pickle** – Maintainable serialization for custom types  

Use these tools to write code that is both **correct and efficient**, leaning on the standard library instead of reinventing data structures.
