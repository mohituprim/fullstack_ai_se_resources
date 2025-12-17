# Comprehensions and Generators: Effective Python Best Practices

## 1. Use Comprehensions Instead of map and filter

### Explanation
List, dict, and set comprehensions are more Pythonic and readable than `map()` and `filter()`. They're also more flexible, allowing multiple conditions and transformations in one expression.

### Use Cases
- Transforming sequences
- Filtering data
- Creating new collections
- Replacing map/filter patterns

### Examples

```python
# ❌ BAD: Using map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

# ✅ GOOD: Using list comprehension
numbers = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in numbers]

# ❌ BAD: Using filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))

# ✅ GOOD: Using list comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]

# Combining map and filter
# ❌ BAD: Using map and filter together
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))

# ✅ GOOD: Single comprehension (much clearer!)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [x ** 2 for x in numbers if x % 2 == 0]

# Dictionary comprehensions
# ❌ BAD: Using map for dict
names = ['Alice', 'Bob', 'Charlie']
name_lengths = dict(map(lambda n: (n, len(n)), names))

# ✅ GOOD: Dictionary comprehension
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}

# Set comprehensions
# ❌ BAD: Using map and set
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squared = set(map(lambda x: x ** 2, numbers))

# ✅ GOOD: Set comprehension
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squared = {x ** 2 for x in numbers}

# Complex transformations
# ✅ GOOD: Comprehensions handle complex logic easily
data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
adult_names = [person['name'] for person in data if person['age'] >= 18]
# Much clearer than map/filter combination!
```

### Benefits
- **Readability**: More Pythonic and easier to understand
- **Flexibility**: Can combine multiple operations
- **Performance**: Often faster than map/filter
- **Consistency**: Same syntax for list, dict, set

---

## 2. Avoid More Than Two Control Subexpressions in Comprehensions

### Explanation
Comprehensions with too many nested conditions or transformations become hard to read. When complexity increases, use regular loops or helper functions instead.

### Use Cases
- Maintaining code readability
- Avoiding overly complex comprehensions
- Making code maintainable
- Balancing conciseness and clarity

### Examples

```python
# ✅ GOOD: Simple comprehension
numbers = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in numbers]

# ✅ GOOD: One condition
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]

# ✅ GOOD: One condition, one transformation
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared_evens = [x ** 2 for x in numbers if x % 2 == 0]

# ⚠️ CAUTION: Two conditions (still readable)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [x ** 2 for x in numbers if x % 2 == 0 if x > 5]  # Two conditions

# ❌ BAD: Too many nested conditions (hard to read)
data = [
    {'name': 'Alice', 'age': 25, 'score': 85, 'active': True},
    {'name': 'Bob', 'age': 30, 'score': 92, 'active': True},
    {'name': 'Charlie', 'age': 22, 'score': 78, 'active': False},
]
result = [
    person['name'].upper() 
    for person in data 
    if person['active'] 
    if person['age'] >= 18 
    if person['score'] > 80
    if len(person['name']) > 4
]
# Too many conditions - hard to understand!

# ✅ GOOD: Break into helper function
def is_valid_person(person):
    return (
        person['active'] and
        person['age'] >= 18 and
        person['score'] > 80 and
        len(person['name']) > 4
    )

result = [person['name'].upper() for person in data if is_valid_person(person)]

# ✅ BETTER: Use regular loop for complex logic
result = []
for person in data:
    if (person['active'] and 
        person['age'] >= 18 and 
        person['score'] > 80 and 
        len(person['name']) > 4):
        result.append(person['name'].upper())

# Nested comprehensions
# ⚠️ CAUTION: One level of nesting is usually OK
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]

# ❌ BAD: Too deeply nested
data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
flattened = [item for group in data for sublist in group for item in sublist]
# Hard to read!

# ✅ GOOD: Use helper function or itertools
from itertools import chain
flattened = list(chain.from_iterable(chain.from_iterable(data)))
```

### Best Practices
- **Keep it simple**: 1-2 conditions max
- **Use helper functions**: For complex logic
- **Prefer loops**: When comprehensions get too complex
- **Readability first**: Clarity over conciseness

---

## 3. Reduce Repetition in Comprehensions with Assignment Expressions

### Explanation
The walrus operator (`:=`) in Python 3.8+ allows you to assign and use a value in the same expression, reducing repetition in comprehensions when you need to use a computed value multiple times.

### Use Cases
- Avoiding repeated function calls
- Caching computed values
- Improving performance
- Reducing code duplication

### Examples

```python
# ❌ BAD: Calling function twice
def expensive_calculation(x):
    print(f"Calculating for {x}")  # Simulate expensive operation
    return x ** 2 + 10

numbers = [1, 2, 3, 4, 5]
result = [expensive_calculation(n) for n in numbers if expensive_calculation(n) > 15]
# expensive_calculation called twice for each number!

# ✅ GOOD: Using assignment expression (walrus operator)
numbers = [1, 2, 3, 4, 5]
result = [value for n in numbers if (value := expensive_calculation(n)) > 15]
# expensive_calculation called only once per number!

# Filtering and transforming
# ❌ BAD: Repeated computation
data = ['apple', 'banana', 'cherry', 'date']
result = [len(word) for word in data if len(word) > 5]
# len() called twice for each word

# ✅ GOOD: Using walrus operator
result = [length for word in data if (length := len(word)) > 5]
# len() called only once

# Complex conditions
# ❌ BAD: Multiple function calls
def get_score(item):
    return item.get('score', 0)

items = [
    {'name': 'A', 'score': 85},
    {'name': 'B', 'score': 92},
    {'name': 'C', 'score': 78},
]
high_scores = [
    item['name'] 
    for item in items 
    if get_score(item) > 80 and get_score(item) < 90
]
# get_score called twice!

# ✅ GOOD: Cache the value
high_scores = [
    item['name']
    for item in items
    if (score := get_score(item)) > 80 and score < 90
]

# Nested comprehensions
# ❌ BAD: Repeated calculation
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = [
    cell * 2 
    for row in matrix 
    for cell in row 
    if sum(row) > 10 and cell * 2 > 10
]
# sum(row) and cell * 2 calculated multiple times

# ✅ GOOD: Using assignment expressions
result = [
    doubled
    for row in matrix
    if (row_sum := sum(row)) > 10
    for cell in row
    if (doubled := cell * 2) > 10
]
```

### Benefits
- **Performance**: Avoids redundant calculations
- **Clarity**: Makes it clear you're reusing a value
- **Efficiency**: Especially important for expensive operations

---

## 4. Consider Generators Instead of Returning Lists

### Explanation
Generator functions use `yield` instead of `return` and produce values lazily. They're memory-efficient for large datasets and can improve performance when you don't need all values at once.

### Use Cases
- Processing large datasets
- Memory-constrained environments
- Streaming data processing
- When you might not need all results

### Examples

```python
# ❌ BAD: Returning list (loads everything into memory)
def read_large_file(filename):
    results = []
    with open(filename) as f:
        for line in f:
            if 'ERROR' in line:
                results.append(line.strip())
    return results  # Entire list in memory!

# ✅ GOOD: Using generator (lazy evaluation)
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            if 'ERROR' in line:
                yield line.strip()  # Yields one at a time

# Process file without loading all into memory
for error_line in read_large_file('huge.log'):
    process(error_line)

# Infinite sequences
# ❌ BAD: Can't create infinite list
def fibonacci_list(n):
    # Must specify limit
    pass

# ✅ GOOD: Generator can be infinite
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use with islice to get first N
from itertools import islice
first_10 = list(islice(fibonacci(), 10))

# Processing pipelines
# ❌ BAD: Creating intermediate lists
def process_data(data):
    step1 = [x * 2 for x in data]  # List 1
    step2 = [x + 10 for x in step1]  # List 2
    step3 = [x for x in step2 if x > 20]  # List 3
    return step3  # All lists in memory!

# ✅ GOOD: Generator pipeline
def process_data(data):
    for x in data:
        x = x * 2      # Step 1
        x = x + 10     # Step 2
        if x > 20:     # Step 3
            yield x    # One value at a time

# Memory comparison
# List: O(n) memory
# Generator: O(1) memory

# When to use lists
# ✅ GOOD: Use list when you need all values
def get_all_users():
    return [user for user in database.get_users()]  # Need all users

# ✅ GOOD: Use generator when streaming
def stream_logs():
    for log in log_source:
        yield process_log(log)  # Process as they come
```

### Benefits
- **Memory efficient**: O(1) vs O(n) memory
- **Lazy evaluation**: Values computed on demand
- **Composable**: Can chain generators
- **Infinite sequences**: Can represent infinite data

---

## 5. Consider Generator Expressions for Large List Comprehensions

### Explanation
Generator expressions (comprehensions in parentheses) are like list comprehensions but produce generators. Use them when you don't need the full list immediately or when memory is a concern.

### Use Cases
- Large datasets
- Memory-constrained situations
- When you only iterate once
- Chaining operations

### Examples

```python
# List comprehension (eager - creates full list)
# ❌ BAD: For large datasets
large_list = [x ** 2 for x in range(1000000)]  # Creates million-item list!
# Memory: ~8MB for integers

# Generator expression (lazy - creates generator)
# ✅ GOOD: Memory efficient
large_gen = (x ** 2 for x in range(1000000))  # Generator object
# Memory: ~100 bytes

# Using generator expressions
# ✅ GOOD: When you only iterate once
total = sum(x ** 2 for x in range(1000000))  # No intermediate list!

# ✅ GOOD: Chaining operations
numbers = range(1000000)
squared = (x ** 2 for x in numbers)
filtered = (x for x in squared if x % 2 == 0)
result = sum(filtered)  # All lazy, no intermediate lists!

# File processing
# ❌ BAD: List comprehension loads all lines
with open('large_file.txt') as f:
    long_lines = [line.strip() for line in f if len(line) > 100]
    # All lines in memory!

# ✅ GOOD: Generator expression processes one at a time
with open('large_file.txt') as f:
    long_lines = (line.strip() for line in f if len(line) > 100)
    for line in long_lines:
        process(line)  # One at a time

# When to use list vs generator
# ✅ Use LIST when:
# - You need to iterate multiple times
# - You need indexing/slicing
# - You need length
# - You need all values at once

squares_list = [x ** 2 for x in range(10)]
print(squares_list[5])      # Can index
print(len(squares_list))    # Can get length
for x in squares_list:      # Can iterate multiple times
    pass

# ✅ Use GENERATOR when:
# - You only iterate once
# - Memory is a concern
# - You're chaining operations
# - You might not need all values

squares_gen = (x ** 2 for x in range(10))
# print(squares_gen[5])     # TypeError - can't index
# print(len(squares_gen))   # TypeError - no length
for x in squares_gen:        # Can iterate once
    pass
# for x in squares_gen:     # Generator exhausted!
#     pass
```

### Key Differences
- **List comprehension** `[...]`: Eager, creates list, can reuse
- **Generator expression** `(...)`: Lazy, creates generator, one-time use

---

## 6. Compose Multiple Generators with yield from

### Explanation
`yield from` (Python 3.3+) delegates to another generator, making it easy to compose generators and flatten nested generators. It's cleaner than manually iterating and yielding.

### Use Cases
- Composing generators
- Flattening nested generators
- Delegating to sub-generators
- Creating generator pipelines

### Examples

```python
# ❌ BAD: Manually iterating and yielding
def numbers():
    yield 1
    yield 2
    yield 3

def more_numbers():
    yield 4
    yield 5
    yield 6

def all_numbers():
    for num in numbers():
        yield num
    for num in more_numbers():
        yield num

# ✅ GOOD: Using yield from
def all_numbers():
    yield from numbers()
    yield from more_numbers()

list(all_numbers())  # [1, 2, 3, 4, 5, 6]

# Flattening nested structures
# ❌ BAD: Manual flattening
def flatten_bad(nested):
    for sublist in nested:
        for item in sublist:
            yield item

# ✅ GOOD: Using yield from
def flatten(nested):
    for sublist in nested:
        yield from sublist

nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
list(flatten(nested))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Recursive flattening
# ✅ GOOD: yield from works recursively
def deep_flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from deep_flatten(item)
        else:
            yield item

deep_nested = [1, [2, [3, 4], 5], 6]
list(deep_flatten(deep_nested))  # [1, 2, 3, 4, 5, 6]

# Generator pipelines
# ✅ GOOD: Composing generators
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith('#'):
            yield line

def add_line_numbers(lines):
    for i, line in enumerate(lines, 1):
        yield f"{i}: {line}"

# Compose with yield from
def process_file(filename):
    lines = read_lines(filename)
    filtered = filter_comments(lines)
    yield from add_line_numbers(filtered)

# Or chain directly
def process_file_simple(filename):
    yield from add_line_numbers(
        filter_comments(
            read_lines(filename)
        )
    )
```

### Benefits
- **Cleaner code**: Less boilerplate
- **Efficient**: No intermediate lists
- **Composable**: Easy to chain generators
- **Readable**: Clear delegation

---

## 7. Pass Iterators into Generators as Arguments Instead of Calling the send Method

### Explanation
The `send()` method for generators is complex and rarely needed. It's clearer to pass iterators as arguments to generator functions, making the code more straightforward and maintainable.

### Use Cases
- Writing clear generator code
- Avoiding complex generator.send() patterns
- Making generators more testable
- Simplifying generator logic

### Examples

```python
# ❌ BAD: Using generator.send() (complex)
def process_data():
    result = yield
    while True:
        if result is None:
            break
        processed = result * 2
        result = yield processed

gen = process_data()
next(gen)  # Prime the generator
result1 = gen.send(10)  # Send value, get result
result2 = gen.send(20)
# Complex and error-prone!

# ✅ GOOD: Pass iterator as argument
def process_data(data):
    for item in data:
        yield item * 2

data = [10, 20, 30]
results = list(process_data(data))  # [20, 40, 60]
# Much simpler!

# Processing with state
# ❌ BAD: Using send() for state
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)
acc.send(10)  # total = 10
acc.send(20)  # total = 30
final = acc.send(None)  # Get final total

# ✅ GOOD: Pass iterator
def accumulator(values):
    total = 0
    for value in values:
        total += value
        yield total

values = [10, 20, 30]
totals = list(accumulator(values))  # [10, 30, 60]

# Filtering and transforming
# ❌ BAD: Complex send() pattern
def filter_and_transform():
    data = yield
    while True:
        if data is None:
            break
        if data > 0:
            result = data ** 2
            data = yield result
        else:
            data = yield None

# ✅ GOOD: Simple iterator argument
def filter_and_transform(data):
    for item in data:
        if item > 0:
            yield item ** 2

numbers = [-2, -1, 0, 1, 2, 3]
results = list(filter_and_transform(numbers))  # [1, 4, 9]
```

### When send() Might Be Appropriate
- Coroutines (async/await is better)
- Two-way communication (rare)
- Complex state machines (consider classes instead)

### Best Practice
- ✅ **Pass iterators**: For most cases
- ❌ **Avoid send()**: Unless you have a specific need
- ✅ **Use classes**: For complex stateful generators

---

## 8. Manage Iterative State Transitions with a Class Instead of the Generator throw Method

### Explanation
The `throw()` method for generators is complex and rarely needed. For stateful iteration with complex state transitions, use a class with `__iter__` and `__next__` methods instead.

### Use Cases
- Complex state machines
- Stateful iteration
- When generator.throw() would be needed
- Making state transitions explicit

### Examples

```python
# ❌ BAD: Using generator with throw() (complex)
def state_machine():
    state = 'start'
    try:
        while True:
            if state == 'start':
                value = yield 'started'
                state = 'processing'
            elif state == 'processing':
                value = yield 'processing'
                if value == 'error':
                    raise ValueError("Error occurred")
                state = 'done'
            elif state == 'done':
                yield 'done'
                break
    except ValueError as e:
        state = 'error'
        yield f'error: {e}'

# Complex and hard to understand!

# ✅ GOOD: Using class (clear state management)
class StateMachine:
    def __init__(self):
        self.state = 'start'
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.state == 'start':
            self.state = 'processing'
            return 'started'
        elif self.state == 'processing':
            self.state = 'done'
            return 'processing'
        elif self.state == 'done':
            raise StopIteration
        else:
            raise StopIteration
    
    def handle_error(self, error):
        self.state = 'error'
        return f'error: {error}'

# Much clearer!
machine = StateMachine()
for state in machine:
    print(state)
    if state == 'processing':
        machine.handle_error("Something went wrong")

# Counter with reset
# ❌ BAD: Generator with throw() for reset
def counter_with_reset():
    count = 0
    try:
        while True:
            count += 1
            reset = yield count
            if reset:
                count = 0
    except GeneratorExit:
        pass

# ✅ GOOD: Class-based counter
class Counter:
    def __init__(self):
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.count += 1
        return self.count
    
    def reset(self):
        self.count = 0

counter = Counter()
for i, value in enumerate(counter):
    print(value)
    if i >= 4:
        counter.reset()
        break

# Iterator with error handling
# ✅ GOOD: Class makes error handling clear
class SafeIterator:
    def __init__(self, data):
        self.data = iter(data)
        self.error_count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return next(self.data)
        except StopIteration:
            raise
        except Exception as e:
            self.error_count += 1
            if self.error_count > 5:
                raise
            return None  # Skip error, continue
```

### Benefits
- **Clarity**: State is explicit in class attributes
- **Maintainability**: Easier to understand and modify
- **Testability**: Easier to test state transitions
- **Flexibility**: Can add methods for state manipulation

---

## Summary

These eight principles help you work effectively with comprehensions and generators:

1. **Comprehensions over map/filter** - More Pythonic and readable
2. **Limit complexity** - Avoid more than 2 control subexpressions
3. **Assignment expressions** - Use walrus operator to reduce repetition
4. **Generators for large data** - Memory-efficient lazy evaluation
5. **Generator expressions** - Use for large datasets and one-time iteration
6. **yield from** - Compose generators cleanly
7. **Pass iterators** - Avoid complex send() patterns
8. **Classes for state** - Use classes instead of generator.throw()

Remember: **Prioritize readability and memory efficiency when working with data transformations.**
