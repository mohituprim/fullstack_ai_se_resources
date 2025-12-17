# Loops and Iterators: Effective Python Best Practices

## 1. Prefer enumerate over range

### Explanation
When you need both the index and value from a sequence, `enumerate()` is more Pythonic and readable than using `range(len())`. It returns tuples of (index, value) pairs.

### Use Cases
- Iterating with indices
- Tracking position in loops
- Processing sequences with position information
- Replacing `range(len())` patterns

### Examples

```python
items = ["apple", "banana", "cherry", "date"]

# ❌ BAD: Using range(len())
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# ✅ GOOD: Using enumerate
for i, item in enumerate(items):
    print(f"{i}: {item}")

# enumerate with start index
# ✅ GOOD: Starting from custom index
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")  # Starts from 1 instead of 0

# Finding items with their indices
# ❌ BAD: Using range
target = "cherry"
for i in range(len(items)):
    if items[i] == target:
        print(f"Found at index {i}")

# ✅ GOOD: Using enumerate
for i, item in enumerate(items):
    if item == target:
        print(f"Found at index {i}")

# Processing with conditions
# ✅ GOOD: enumerate with conditions
numbers = [10, 20, 30, 40, 50]
for index, value in enumerate(numbers):
    if value > 25:
        print(f"Index {index} has value {value}")

# Building dictionaries with indices
# ✅ GOOD: Using enumerate for dict creation
items = ["apple", "banana", "cherry"]
item_dict = {index: item for index, item in enumerate(items)}
print(item_dict)  # {0: 'apple', 1: 'banana', 2: 'cherry'}

# Tracking progress
# ✅ GOOD: Using enumerate for progress tracking
items = ["task1", "task2", "task3", "task4", "task5"]
for i, task in enumerate(items, start=1):
    print(f"Processing {i}/{len(items)}: {task}")
```

### Benefits
- More readable and Pythonic
- Avoids index errors
- Can specify start index
- Works with any iterable

---

## 2. Use zip to Process Iterators in Parallel

### Explanation
`zip()` combines multiple iterables element-wise, allowing you to process corresponding elements together. It stops when the shortest iterable is exhausted.

### Use Cases
- Processing corresponding elements from multiple sequences
- Combining data from different sources
- Iterating over multiple lists simultaneously
- Building dictionaries from two lists

### Examples

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]
cities = ["New York", "London", "Paris"]

# ❌ BAD: Using indices
for i in range(len(names)):
    print(f"{names[i]} is {ages[i]} years old, lives in {cities[i]}")

# ✅ GOOD: Using zip
for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old, lives in {city}")

# Building dictionaries
# ✅ GOOD: Creating dict from two lists
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]
name_age_dict = dict(zip(names, ages))
print(name_age_dict)  # {'Alice': 25, 'Bob': 30, 'Charlie': 22}

# Processing with different lengths
# ⚠️ CAUTION: zip stops at shortest iterable
names = ["Alice", "Bob", "Charlie", "David"]
ages = [25, 30, 22]
# Only processes first 3 pairs
for name, age in zip(names, ages):
    print(f"{name}: {age}")

# ✅ GOOD: Using zip_longest for different lengths
from itertools import zip_longest
names = ["Alice", "Bob", "Charlie", "David"]
ages = [25, 30, 22]
for name, age in zip_longest(names, ages, fillvalue="Unknown"):
    print(f"{name}: {age}")

# Unzipping (reverse operation)
# ✅ GOOD: Separating zipped data
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
print(numbers)  # (1, 2, 3)
print(letters)  # ('a', 'b', 'c')

# Transposing matrices
# ✅ GOOD: Using zip to transpose
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = list(zip(*matrix))
print(transposed)  # [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

# Comparing corresponding elements
# ✅ GOOD: Comparing parallel sequences
list1 = [1, 2, 3, 4, 5]
list2 = [1, 2, 4, 4, 5]
differences = [(a, b) for a, b in zip(list1, list2) if a != b]
print(differences)  # [(3, 4)]

# Processing multiple files
# ✅ GOOD: Reading multiple files in parallel
file1_lines = ["line1", "line2", "line3"]
file2_lines = ["data1", "data2", "data3"]
for line1, line2 in zip(file1_lines, file2_lines):
    print(f"{line1} | {line2}")
```

### Key Points
- Stops at shortest iterable
- Returns iterator (use `list()` to materialize)
- Use `zip_longest()` for different lengths
- Can unzip with `zip(*zipped_data)`

---

## 3. Avoid else Blocks After for and while Loops

### Explanation
Python allows `else` blocks after loops, which execute when the loop completes normally (not via `break`). This is confusing and non-intuitive - most developers expect `else` to mean "if condition is false", not "if loop completed".

### Use Cases
- Writing clearer, more maintainable code
- Avoiding confusion for other developers
- Using explicit flags instead of loop-else

### Examples

```python
# ❌ BAD: Using loop-else (confusing)
def find_item(items, target):
    for item in items:
        if item == target:
            print("Found!")
            break
    else:
        print("Not found!")  # Executes if loop completes without break

# ✅ GOOD: Using explicit flag
def find_item(items, target):
    found = False
    for item in items:
        if item == target:
            print("Found!")
            found = True
            break
    if not found:
        print("Not found!")

# ✅ BETTER: Using early return
def find_item(items, target):
    for item in items:
        if item == target:
            print("Found!")
            return
    print("Not found!")

# Prime number check
# ❌ BAD: Using loop-else
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    else:
        return True  # Confusing!

# ✅ GOOD: Clear logic
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True  # Clear: if we get here, it's prime

# Searching with while
# ❌ BAD: while-else
items = [1, 2, 3, 4, 5]
i = 0
while i < len(items):
    if items[i] == 10:
        print("Found!")
        break
    i += 1
else:
    print("Not found!")  # Confusing!

# ✅ GOOD: Explicit flag
items = [1, 2, 3, 4, 5]
found = False
i = 0
while i < len(items):
    if items[i] == 10:
        print("Found!")
        found = True
        break
    i += 1
if not found:
    print("Not found!")
```

### Why Avoid
- **Confusing**: `else` suggests "if condition false", not "if loop completed"
- **Non-intuitive**: Most developers don't expect this behavior
- **Maintainability**: Harder for others to understand
- **Alternatives**: Flags or early returns are clearer

---

## 4. Never Use for Loop Variables After the Loop Ends

### Explanation
Loop variables persist after the loop completes and retain their last value. Relying on this creates fragile code that's hard to debug. The variable may not exist if the loop never runs.

### Use Cases
- Writing robust code
- Avoiding subtle bugs
- Making code maintainable
- Following best practices

### Examples

```python
# ❌ BAD: Using loop variable after loop
items = [1, 2, 3, 4, 5]
for item in items:
    if item > 3:
        break

print(f"Last processed: {item}")  # Dangerous! What if loop never ran?

# ✅ GOOD: Explicit tracking
items = [1, 2, 3, 4, 5]
last_item = None
for item in items:
    if item > 3:
        last_item = item
        break

if last_item is not None:
    print(f"Last processed: {last_item}")

# Finding last item
# ❌ BAD: Relying on loop variable
items = []
for item in items:
    process(item)
print(f"Last: {item}")  # NameError if items is empty!

# ✅ GOOD: Explicit handling
items = []
last_item = None
for item in items:
    process(item)
    last_item = item

if last_item is not None:
    print(f"Last: {last_item}")

# Loop that might not execute
# ❌ BAD: Assuming variable exists
for i in range(0):  # Empty range!
    do_something(i)
print(i)  # NameError!

# ✅ GOOD: Check if loop executed
i = None
for i in range(0):
    do_something(i)
if i is not None:
    print(i)

# Nested loops
# ❌ BAD: Using outer loop variable
for i in range(3):
    for j in range(2):
        if some_condition():
            break
    print(f"Outer: {i}, Inner: {j}")  # j might not be what you expect!

# ✅ GOOD: Explicit tracking
for i in range(3):
    last_j = None
    for j in range(2):
        if some_condition():
            last_j = j
            break
    if last_j is not None:
        print(f"Outer: {i}, Inner: {last_j}")
```

### Best Practices
1. **Don't rely** on loop variables after the loop
2. **Use explicit variables** to track what you need
3. **Check if variables exist** before using them
4. **Use functions** to encapsulate loop logic

---

## 5. Be Defensive when Iterating over Arguments

### Explanation
Functions that iterate over arguments multiple times can fail if passed iterators (which are consumed after first iteration). Be defensive by converting to lists or checking types.

### Use Cases
- Writing robust functions
- Handling both lists and iterators
- Preventing subtle bugs
- Making functions more flexible

### Examples

```python
# ❌ BAD: Iterating multiple times (fails with iterators)
def normalize(numbers):
    total = sum(numbers)  # First iteration - consumes iterator
    result = []
    for value in numbers:  # Second iteration - iterator is empty!
        percent = 100 * value / total
        result.append(percent)
    return result

# This works with lists
normalize([1, 2, 3, 4, 5])  # OK

# This fails with iterators
normalize(iter([1, 2, 3, 4, 5]))  # Fails! Iterator consumed

# ✅ GOOD: Convert to list first
def normalize(numbers):
    numbers = list(numbers)  # Convert to list (works with any iterable)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# ✅ GOOD: Using generator expression (memory efficient for large data)
def normalize(numbers):
    numbers = list(numbers)  # Materialize once
    total = sum(numbers)
    return [100 * value / total for value in numbers]

# Checking if iterator
# ✅ GOOD: Defensive check
def process_data(data):
    if not isinstance(data, (list, tuple)):
        data = list(data)  # Convert iterators/generators to list
    # Now safe to iterate multiple times
    return sum(data), max(data), min(data)

# Generator functions
# ❌ BAD: Multiple iterations of generator
def get_stats(numbers):
    return {
        'sum': sum(numbers),      # Consumes generator
        'max': max(numbers),       # Generator already consumed!
        'min': min(numbers)       # Generator already consumed!
    }

# ✅ GOOD: Materialize once
def get_stats(numbers):
    numbers = list(numbers)  # Convert to list
    return {
        'sum': sum(numbers),
        'max': max(numbers),
        'min': min(numbers)
    }

# File reading
# ❌ BAD: Multiple iterations
def process_file_lines(file):
    lines = file.readlines()  # Returns list - OK
    count = len(lines)
    total_chars = sum(len(line) for line in lines)
    return count, total_chars

# ✅ GOOD: Handle both file objects and lists
def process_file_lines(file_or_lines):
    if hasattr(file_or_lines, 'readlines'):
        lines = file_or_lines.readlines()
    else:
        lines = list(file_or_lines)  # Convert iterator to list
    
    count = len(lines)
    total_chars = sum(len(line) for line in lines)
    return count, total_chars
```

### Key Points
- Iterators are consumed after first iteration
- Convert to `list()` if you need multiple passes
- Check types if you need to handle both lists and iterators
- Document if your function consumes iterators

---

## 6. Never Modify Containers While Iterating over Them; Use Copies or Caches Instead

### Explanation
Modifying a container (list, dict, set) while iterating over it can cause unpredictable behavior, skipped elements, or runtime errors. Always iterate over a copy or collect changes to apply later.

### Use Cases
- Removing items during iteration
- Adding items during iteration
- Modifying dictionary keys during iteration
- Writing safe iteration code

### Examples

```python
# ❌ BAD: Modifying list while iterating
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Dangerous! Modifies list during iteration
print(items)  # Unpredictable result

# ✅ GOOD: Iterate over copy
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for item in items[:]:  # Slice creates copy
    if item % 2 == 0:
        items.remove(item)
print(items)  # [1, 3, 5, 7, 9]

# ✅ BETTER: List comprehension (more Pythonic)
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
items = [item for item in items if item % 2 != 0]
print(items)  # [1, 3, 5, 7, 9]

# Removing from dictionary
# ❌ BAD: Modifying dict while iterating
data = {"a": 1, "b": 2, "c": 3, "d": 4}
for key in data:
    if data[key] % 2 == 0:
        del data[key]  # RuntimeError: dictionary changed size during iteration

# ✅ GOOD: Iterate over copy of keys
data = {"a": 1, "b": 2, "c": 3, "d": 4}
for key in list(data.keys()):  # Create list of keys first
    if data[key] % 2 == 0:
        del data[key]
print(data)  # {'a': 1, 'c': 3}

# ✅ BETTER: Dictionary comprehension
data = {"a": 1, "b": 2, "c": 3, "d": 4}
data = {k: v for k, v in data.items() if v % 2 != 0}
print(data)  # {'a': 1, 'c': 3}

# Adding items during iteration
# ❌ BAD: Adding to list while iterating
items = [1, 2, 3]
for item in items:
    items.append(item * 2)  # Infinite loop risk!
    if len(items) > 10:
        break

# ✅ GOOD: Collect changes, apply after
items = [1, 2, 3]
to_add = []
for item in items:
    to_add.append(item * 2)
items.extend(to_add)
print(items)  # [1, 2, 3, 2, 4, 6]

# Modifying nested structures
# ❌ BAD: Modifying while iterating
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    row.append(sum(row))  # This is OK (modifying row, not matrix)
    matrix.append([0, 0, 0])  # This is BAD (modifying matrix)
    if len(matrix) > 5:
        break

# ✅ GOOD: Collect changes
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
new_rows = []
for row in matrix:
    row.append(sum(row))  # OK - modifying row content
    new_rows.append([0, 0, 0])
matrix.extend(new_rows)

# Sets
# ❌ BAD: Modifying set while iterating
numbers = {1, 2, 3, 4, 5}
for num in numbers:
    if num % 2 == 0:
        numbers.discard(num)  # RuntimeError!

# ✅ GOOD: Iterate over copy
numbers = {1, 2, 3, 4, 5}
for num in list(numbers):  # Convert to list
    if num % 2 == 0:
        numbers.discard(num)
print(numbers)  # {1, 3, 5}

# ✅ BETTER: Set comprehension
numbers = {1, 2, 3, 4, 5}
numbers = {num for num in numbers if num % 2 != 0}
print(numbers)  # {1, 3, 5}
```

### Best Practices
1. **Never modify** container while iterating
2. **Use copies** (`list()`, `dict.copy()`, `set.copy()`, or slicing)
3. **Use comprehensions** for filtering/transforming
4. **Collect changes** and apply after iteration

---

## 7. Pass Iterators to any and all for Efficient Short-Circuiting Logic

### Explanation
`any()` and `all()` support short-circuiting - they stop as soon as the result is determined. Passing iterators (not lists) allows them to stop early without evaluating all elements, saving computation.

### Use Cases
- Checking conditions efficiently
- Early termination of expensive operations
- Memory-efficient condition checking
- Performance optimization

### Examples

```python
# ✅ GOOD: Using any() with generator (short-circuits)
def has_positive(numbers):
    return any(n > 0 for n in numbers)  # Stops at first positive

numbers = [-1, -2, -3, 4, 5, 6]
print(has_positive(numbers))  # True, stops after finding 4

# ❌ BAD: Converting to list first (no short-circuit benefit)
def has_positive(numbers):
    numbers_list = list(numbers)  # Evaluates all!
    return any(n > 0 for n in numbers_list)

# ✅ GOOD: Using all() with generator
def all_positive(numbers):
    return all(n > 0 for n in numbers)  # Stops at first non-positive

numbers = [1, 2, 3, -1, 5]
print(all_positive(numbers))  # False, stops at -1

# Expensive operations
# ✅ GOOD: Short-circuiting expensive operations
def expensive_check(n):
    print(f"Checking {n}")  # Simulate expensive operation
    return n > 100

numbers = [1, 2, 3, 200, 4, 5]
result = any(expensive_check(n) for n in numbers)
# Only prints: "Checking 1", "Checking 2", "Checking 3", "Checking 200"
# Stops after finding first True

# File processing
# ✅ GOOD: Early exit with any()
def file_has_error(file_path):
    with open(file_path) as f:
        return any('ERROR' in line for line in f)  # Stops at first error

# Multiple conditions
# ✅ GOOD: Combining conditions efficiently
def is_valid_user(user):
    checks = [
        user.get('name'),
        user.get('email'),
        len(user.get('password', '')) >= 8,
        user.get('age', 0) >= 18
    ]
    return all(checks)  # Stops at first False

# Real-world example
# ✅ GOOD: Checking if any item matches
items = [
    {'name': 'apple', 'price': 1.0},
    {'name': 'banana', 'price': 0.5},
    {'name': 'cherry', 'price': 2.0}
]

has_expensive = any(item['price'] > 1.5 for item in items)
print(has_expensive)  # True, stops after cherry

# Complex conditions
# ✅ GOOD: Nested conditions with short-circuiting
def process_data(data):
    # Only processes if all conditions met, stops early if any fail
    if all(
        item.get('value', 0) > 0
        and item.get('status') == 'active'
        for item in data
    ):
        return "All items valid"
    return "Some items invalid"
```

### Benefits
- **Performance**: Stops early when result is known
- **Memory**: Doesn't need to materialize entire list
- **Efficiency**: Avoids unnecessary computations
- **Readability**: Clear intent

---

## 8. Consider itertools for Working with Iterators and Generators

### Explanation
The `itertools` module provides powerful tools for working with iterators and generators. These functions are optimized, memory-efficient, and can replace complex custom iteration logic.

### Use Cases
- Complex iteration patterns
- Memory-efficient processing
- Combining/transforming iterators
- Replacing custom iteration code

### Examples

```python
from itertools import chain, combinations, permutations, cycle, repeat, islice, groupby

# chain - Combine multiple iterables
# ✅ GOOD: Flattening lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]
combined = list(chain(list1, list2, list3))
print(combined)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ✅ GOOD: Flattening nested structure
nested = [[1, 2], [3, 4], [5, 6]]
flattened = list(chain.from_iterable(nested))
print(flattened)  # [1, 2, 3, 4, 5, 6]

# combinations - All combinations
# ✅ GOOD: Getting combinations
items = ['a', 'b', 'c']
combs = list(combinations(items, 2))
print(combs)  # [('a', 'b'), ('a', 'c'), ('b', 'c')]

# permutations - All permutations
# ✅ GOOD: Getting permutations
perms = list(permutations(items, 2))
print(perms)  # [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]

# cycle - Infinite cycle
# ✅ GOOD: Cycling through values
colors = cycle(['red', 'green', 'blue'])
for i, color in enumerate(colors):
    if i >= 10:
        break
    print(color)  # red, green, blue, red, green, blue, ...

# repeat - Repeat value
# ✅ GOOD: Repeating values
ones = list(islice(repeat(1), 5))
print(ones)  # [1, 1, 1, 1, 1]

# islice - Slice iterator
# ✅ GOOD: Slicing without materializing
numbers = range(100)
first_10 = list(islice(numbers, 10))
print(first_10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

every_other = list(islice(numbers, 0, 20, 2))
print(every_other)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# groupby - Group consecutive elements
# ✅ GOOD: Grouping data
data = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4]
grouped = {key: list(group) for key, group in groupby(data)}
print(grouped)  # {1: [1, 1, 1], 2: [2, 2], 3: [3, 3, 3, 3], 4: [4]}

# More itertools functions
from itertools import count, takewhile, dropwhile, zip_longest, product

# count - Infinite counter
# ✅ GOOD: Generating sequence
numbers = list(islice(count(10, 2), 5))  # Start at 10, step by 2
print(numbers)  # [10, 12, 14, 16, 18]

# takewhile - Take while condition true
# ✅ GOOD: Taking elements while condition holds
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(takewhile(lambda x: x < 6, numbers))
print(result)  # [1, 2, 3, 4, 5]

# dropwhile - Drop while condition true
# ✅ GOOD: Skipping elements while condition holds
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(dropwhile(lambda x: x < 6, numbers))
print(result)  # [6, 7, 8, 9, 10]

# zip_longest - Zip with fillvalue
# ✅ GOOD: Zipping different length iterables
list1 = [1, 2, 3]
list2 = ['a', 'b']
result = list(zip_longest(list1, list2, fillvalue='-'))
print(result)  # [(1, 'a'), (2, 'b'), (3, '-')]

# product - Cartesian product
# ✅ GOOD: All combinations from multiple iterables
colors = ['red', 'blue']
sizes = ['S', 'M', 'L']
combinations = list(product(colors, sizes))
print(combinations)  # [('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ...]

# Real-world example: Processing chunks
# ✅ GOOD: Processing data in chunks
def process_in_chunks(data, chunk_size=3):
    it = iter(data)
    while True:
        chunk = list(islice(it, chunk_size))
        if not chunk:
            break
        yield chunk

data = list(range(10))
for chunk in process_in_chunks(data, 3):
    print(chunk)  # [0, 1, 2], [3, 4, 5], [6, 7, 8], [9]
```

### Key itertools Functions
- **chain**: Combine iterables
- **combinations/permutations**: Generate combinations
- **cycle/repeat**: Infinite iterators
- **islice**: Slice without materializing
- **groupby**: Group consecutive elements
- **takewhile/dropwhile**: Conditional iteration
- **product**: Cartesian product

### Benefits
- **Optimized**: C implementations for performance
- **Memory-efficient**: Work with iterators, not lists
- **Readable**: Clear, expressive code
- **Powerful**: Handle complex iteration patterns

---

## Summary

These eight principles help you write effective loops and work with iterators:

1. **enumerate** - Prefer over `range(len())` for index-value pairs
2. **zip** - Process multiple iterables in parallel
3. **Avoid loop-else** - Use explicit flags or early returns
4. **Don't use loop variables after loop** - Use explicit tracking
5. **Be defensive with arguments** - Convert iterators to lists if needed multiple times
6. **Never modify during iteration** - Use copies or comprehensions
7. **any/all with iterators** - Leverage short-circuiting for efficiency
8. **itertools** - Use for complex iteration patterns

Remember: **Write clear, maintainable iteration code that other developers can understand.**
